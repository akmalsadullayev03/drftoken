from django.urls import path
from .views import SignUpView, LoginView, LogoutView, ProfileView, PasswordChangeView

urlpatterns = [
    path('auth/signup/', SignUpView.as_view(), name='signup'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/profile/', ProfileView.as_view(), name='profile'),
    path('auth/password-change/', PasswordChangeView.as_view(), name='password-change'),
]