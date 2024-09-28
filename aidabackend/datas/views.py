from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from .models import User
from .serializers import UserSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()  
        data['password'] = make_password(data['password'])  

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    def post(self, request):
        username = request.data.get('username')  
        password = request.data.get('password')

        try:
            user = User.objects.get(username=username) 
            if check_password(password, user.password):
                return Response({
                    'message': 'Login successful',
                    'token': 'your_jwt_token_here', 
                    'isadmin': user.isadmin 
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
        
class UserListView(generics.ListAPIView):
    queryset = User.objects.filter(isadmin=False)  # Filter out admin users
    serializer_class = UserSerializer