from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView, TokenVerifyView
from django.urls import path

from core.api.views import get_users, register_user, modify_user, get_user, reset_password




urlpatterns = [
    # Login Routes
    path('api/token',TokenObtainPairView.as_view()),
    path('api/token/refresh',TokenRefreshView.as_view()),
    path('api/token/verify',TokenVerifyView.as_view()),
    
    #Getting List of Users
    path('users/',get_users,name='get_users'),
    
    # Creating User
    path('users/register',register_user,name='register_user'),
    
    #Getting Single User
    path('user/<int:pk>', get_user, name='get_user'),
    
    
    #DELETE, PUT, PATCH
    path('users/<int:pk>', modify_user, name='modify_user'),
    
    # Route to change password
    path('users/reset-password',reset_password,name='reset_password')
    
    
]
