from django.urls import path
from .views import RegisterView, LoginView, LogoutView, HomeView, ProfileDetailView, ProfileUpdateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import messages

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<slug:slug>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/<slug:slug>/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
]