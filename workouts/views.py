from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, TemplateView
from django.urls import reverse_lazy
from .models import Workout, UserWorkoutSignup, UserWorkoutHistory
from .forms import WorkoutForm

class WorkoutListView(LoginRequiredMixin, ListView):
    model = Workout
    template_name = 'workouts/workout_list.html'
    context_object_name = 'workouts'

class SignUpForWorkoutView(LoginRequiredMixin, TemplateView):
    template_name = 'workouts/sign_up_for_workout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        workout = get_object_or_404(Workout, slug=kwargs['slug'])
        context['workout'] = workout
        return context

    def post(self, request, slug, *args, **kwargs):
        workout = get_object_or_404(Workout, slug=slug)
        UserWorkoutSignup.objects.create(user=request.user, workout=workout)
        return redirect('workouts_list')

class UserWorkoutHistoryView(LoginRequiredMixin, TemplateView):
    template_name = 'workouts/user_workout_history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['history'] = UserWorkoutHistory.objects.filter(user=self.request.user)
        return context

class TrainerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'workouts/trainer_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.role != 'trainer':
            return redirect('home')
        context['workouts'] = Workout.objects.filter(trainer=self.request.user)
        return context

class WorkoutCreateView(LoginRequiredMixin, CreateView):
    model = Workout
    form_class = WorkoutForm
    template_name = 'workouts/workout_create.html'

    def form_valid(self, form):
        form.instance.trainer = self.request.user  
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('trainer_dashboard')
