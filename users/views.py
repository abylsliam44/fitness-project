from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import DetailView, UpdateView
from django.urls import reverse
from .models import User, Profile
from .forms import RegisterForm, LoginForm, ProfileForm
from .utils import send_welcome_email

class HomeView(View):
    def get(self, request):
        context = {
            "message": "Push Limits. Achieve Goals. Stay Fit!",
        }
        return render(request, 'users/home.html', context)

class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_welcome_email(user)  
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login')
        return render(request, 'users/register.html', {'form': form})

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('home')
            else:
                messages.error(request, "Invalid email or password.")
        return render(request, 'users/login.html', {'form': form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect('home')

class WorkoutsView(View):
    def get(self, request):
        return render(request, 'workouts_list.html')

class MarketplaceView(View):
    def get(self, request):
        return render(request, 'marketplace.html')
    
class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'users/profile_detail.html'
    context_object_name = 'profile'

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'users/profile_edit.html'

    def get_success_url(self):
        return reverse('profile_detail', kwargs={'slug': self.object.slug})

