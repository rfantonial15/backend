from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate,login

from .models import User
from .serializers import UserSerializer, LoginSerializer, RegisterSerializer

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import BasePermission


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        # Manually hash the password before saving
        if 'password' in data:
            data['password'] = make_password(data['password'])
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            user = User.objects.get(email=serializer.data["email"])
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
    authentication_classes = [JWTAuthentication]

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
        
class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        serializer = LoginSerializer(data=request.data)
        try:
            user = User.objects.get(email__iexact=email)
            if user.is_frozen:  # Check if the user is frozen
                return Response({'error': 'Your account is frozen. Please contact the admin.'}, status=status.HTTP_403_FORBIDDEN)
            
            print(user)
            if not user.is_verified:
                return Response({'error': 'Email is not verified.'}, status=status.HTTP_403_FORBIDDEN)

            if serializer.is_valid() and check_password(password, user.password):
                user_login = authenticate(request, email=serializer.data["email"], password=password)
                print(user_login)
                login_response = login(request, user_login)       
                print(login_response)
                refresh = RefreshToken.for_user(user)
                user_data = {
                    'firstname': user.firstname,
                    'lastname': user.lastname,
                    'email': user.email,
                    'username': user.username,
                    'phone': user.phone,
                    'barangay': user.barangay,
                    'isadmin': user.isadmin,
                    'isstaff': user.is_staff,
                    'issuperuser': user.is_superuser,
                    "id":user.id
                }
                return Response({
                    'message': 'Login successful',
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user': user_data,
                    'isadmin': user.isadmin,  # Include this field for frontend to use
                    'isstaff': user.is_staff,
                    'issuperuser': user.is_superuser,
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            print(serializer.errors)
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

class UserListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.filter(isadmin=False)  
    serializer_class = UserSerializer

class UserRoleView(APIView):
    permission_classes = [AllowAny]  # Require authentication

    def get(self, request, *args, **kwargs):
        user = request.user
        return Response({
            'isadmin': user.isadmin,
            'issuperuser': user.is_superuser,
            'isstaff': user.is_staff,
        }, status=status.HTTP_200_OK)


class ResendVerificationView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]

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
    authentication_classes = [JWTAuthentication]

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
    authentication_classes = [JWTAuthentication]
    
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
    authentication_classes = [JWTAuthentication]

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
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Allow unauthenticated users to update data
    authentication_classes = [JWTAuthentication]
    
    def put(self, request, id, *args, **kwargs):
        user_edit = User.objects.get(id=id)
        print(user_edit)
        user = request.user 
        data = request.data
        print(data)

        updatable_fields = ['firstname', 'lastname', 'username', 'phone', 'barangay']
        for field in updatable_fields:
            if field in data:
                setattr(user, field, data[field])

        user.save()

        return Response(
            {"message": "Profile updated successfully", "user": UserSerializer(user).data},
            status=status.HTTP_200_OK
        )

class FreezeUserView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]

    def post(self, request, id):
        try:
            user = User.objects.get(id=id)
            user.is_frozen = True
            user.save(update_fields=["is_frozen"])
            return Response({'message': 'User account has been frozen.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

class UnfreezeUserView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]

    def post(self, request, id):
        try:
            user = User.objects.get(id=id)
            user.is_frozen = False
            user.save(update_fields=["is_frozen"])
            return Response({'message': 'User account has been unfrozen.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

