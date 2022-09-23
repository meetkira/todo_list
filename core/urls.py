from django.contrib import admin
from django.urls import path

from core import views

urlpatterns = [
    path('signup', views.UserCreateView.as_view(), name='create user'),
    path('login', views.LoginView.as_view(), name='login user'),
    path('profile', views.ProfileView.as_view(), name='get/update/delete user'),
    path('update_password', views.ChangePasswordView.as_view(), name='change password'),

]
