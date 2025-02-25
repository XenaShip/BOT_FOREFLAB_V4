from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.apps import UsersConfig
from users.views import UserCreateView, UserDetailView, UserUpdateView, UserDeleteView, UserListView, MyLoginView

app_name = UsersConfig.name

urlpatterns = [
    path('login', MyLoginView.as_view(template_name='users/login.html'), name='login'),
    path('user_list/', UserListView.as_view(), name='user_list'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('user/create/', UserCreateView.as_view(), name='user_create'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('user/<int:pk>/edit/', UserUpdateView.as_view(), name='user_update'),
    path('user/<int:pk>/delete/', UserDeleteView.as_view(), name='user_confirm_delete'),
]