from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from .models import User
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        # Manually hash the password before saving
        if 'password' in data:
            data['password'] = make_password(data['password'])
        
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            # Save the user without calling `serializer.save()` to handle password manually
            user = User(
                firstname=data['firstname'],
                lastname=data['lastname'],
                email=data['email'],
                username=data['username'],
                password=data['password'],  # Hashed password
                phone=data.get('phone', ''),
                barangay=data.get('barangay', ''),
                isadmin=False  # Set any other default values here
            )
            user.save()

            # Generate verification code and send email
            user.generate_verification_code()
            send_mail(
                'Verify Your Email',
                f'Your verification code is: {user.verification_code}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            return Response(
                {'message': 'Account created. Please check your email to verify your account.'},
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        
        try:
            # Check if there is a user with the provided email and verification code
            user = User.objects.get(email=email, verification_code=code)
            
            # Update the user's verification status and clear the code
            user.is_verified = True
            user.verification_code = None
            user.save(update_fields=['is_verified', 'verification_code'])
            
            # Return success response
            return Response({'message': 'Email verified successfully.'}, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            # Return error response if the email or code is incorrect
            return Response({'error': 'Invalid email or verification code.'}, status=status.HTTP_400_BAD_REQUEST)
        
class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email__iexact=email)

            if not user.is_verified:
                return Response({'error': 'Email is not verified.'}, status=status.HTTP_403_FORBIDDEN)

            if check_password(password, user.password):
                refresh = RefreshToken.for_user(user)
                user_data = {
                    'firstname': user.firstname,
                    'lastname': user.lastname,
                    'email': user.email,
                    'username': user.username,
                    'phone': user.phone,
                    'barangay': user.barangay,
                    'isadmin': user.isadmin,
                }
                return Response({
                    'message': 'Login successful',
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user': user_data,
                    'isadmin': user.isadmin,  # Include this field for frontend to use
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

class UserListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.filter(isadmin=False)  
    serializer_class = UserSerializer

class ResendVerificationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        
        try:
            user = User.objects.get(email=email)
            if user.is_verified:
                return Response({'message': 'Account is already verified.'}, status=status.HTTP_400_BAD_REQUEST)
            
            user.generate_verification_code()
            send_mail(
                'Resend: Verify Your Email',
                f'Your new verification code is: {user.verification_code}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            
            return Response({'message': 'Verification email has been resent.'}, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

class RequestPasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            user.generate_verification_code() 
            send_mail(
                'Password Reset Code',
                f'Your password reset code is: {user.verification_code}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )
            return Response({'message': 'Reset code sent to your email.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

class VerifyResetCodeView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        
        try:
            user = User.objects.get(email=email, verification_code=code)
            user.verification_code = None
            user.save(update_fields=['verification_code'])
            return Response({'message': 'Code verified successfully.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Invalid email or reset code.'}, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        new_password = request.data.get('new_password')

        try:
            user = User.objects.get(email=email)
            user.password = make_password(new_password)
            user.save()
            return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
class ProfileUpdateView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated users to update data

    def post(self, request, *args, **kwargs):
        user = request.user  # This will be None if the user is unauthenticated
        data = request.data

        # If user is unauthenticated, you may want to allow them to send the data
        # but that can expose security risks, so be cautious.
        if not user:
            return Response({"error": "You must be logged in to update your profile"}, status=status.HTTP_401_UNAUTHORIZED)

        updatable_fields = ['firstname', 'lastname', 'username', 'phone', 'barangay']
        for field in updatable_fields:
            if field in data:
                setattr(user, field, data[field])

        user.save()

        return Response(
            {"message": "Profile updated successfully", "user": UserSerializer(user).data},
            status=status.HTTP_200_OK
        )