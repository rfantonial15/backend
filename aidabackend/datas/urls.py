# urls.py

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView, LoginView, UserListView, VerifyEmailView, UserRoleView, ResendVerificationView, RequestPasswordResetView, VerifyResetCodeView, ResetPasswordView, ProfileUpdateView, FreezeUserView, UnfreezeUserView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('resend-verification/', ResendVerificationView.as_view(), name='resend-verification'),
    path('request-password-reset/', RequestPasswordResetView.as_view(), name='request-password-reset'),
    path('verify-reset-code/', VerifyResetCodeView.as_view(), name='verify-reset-code'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/update/<str:id>/', ProfileUpdateView.as_view(), name='profile-update'),
    path('users/freeze/<int:id>/', FreezeUserView.as_view(), name='freeze-user'),
    path('users/unfreeze/<int:id>/', UnfreezeUserView.as_view(), name='unfreeze-user'),
    path('user-role/', UserRoleView.as_view(), name='user-role'),
]
