from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, TemplateView, DetailView
from django.urls import reverse_lazy, reverse
from .models import Workout, WorkoutCategory, UserWorkoutSignup, UserWorkoutHistory, WorkoutReview, WorkoutPlan, GroupWorkout, TrainerRating
from .forms import WorkoutForm, WorkoutReviewForm, WorkoutPlanForm, GroupWorkoutForm, TrainerRatingForm


class WorkoutCategoryListView(ListView):
    model = WorkoutCategory
    template_name = 'workouts/category_list.html'
    context_object_name = 'categories'


class WorkoutsByCategoryView(ListView):
    template_name = 'workouts/workouts_by_category.html'
    context_object_name = 'workouts'

    def get_queryset(self):
        self.category = get_object_or_404(WorkoutCategory, slug=self.kwargs['slug'])
        return Workout.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class WorkoutDetailView(DetailView):
    model = Workout
    template_name = 'workouts/workout_detail.html'
    context_object_name = 'workout'
    slug_url_kwarg = 'slug'


class SignUpForWorkoutView(LoginRequiredMixin, TemplateView):
    template_name = 'workouts/sign_up_for_workout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        workout = get_object_or_404(Workout, slug=slug)
        context['workout'] = workout
        context['signed_up'] = workout.is_user_enrolled(self.request.user)
        context['spots_left'] = workout.available_slots()
        return context

    def post(self, request, *args, **kwargs):
        workout = get_object_or_404(Workout, slug=kwargs.get('slug'))
        UserWorkoutSignup.objects.get_or_create(user=request.user, workout=workout)
        return redirect('workout_categories')


class UserWorkoutHistoryView(LoginRequiredMixin, ListView):
    model = UserWorkoutHistory
    template_name = 'workouts/user_workout_history.html'
    context_object_name = 'history'

    def get_queryset(self):
        return UserWorkoutHistory.objects.filter(user=self.request.user)


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


class WorkoutReviewCreateView(CreateView):
    model = WorkoutReview
    form_class = WorkoutReviewForm
    template_name = 'workouts/review_create.html'

    def form_valid(self, form):
        workout = Workout.objects.get(slug=self.kwargs['slug'])
        form.instance.workout = workout
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('workout_detail', kwargs={'slug': self.kwargs['slug']})


class WorkoutPlanCreateView(CreateView):
    model = WorkoutPlan
    form_class = WorkoutPlanForm
    template_name = 'workouts/workout_plan_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('workout_plan_detail', kwargs={'pk': self.object.pk})


class GroupWorkoutCreateView(CreateView):
    model = GroupWorkout
    form_class = GroupWorkoutForm
    template_name = 'workouts/group_workout_create.html'

    def form_valid(self, form):
        form.instance.trainer = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('group_workout_detail', kwargs={'pk': self.object.pk})


class TrainerRatingCreateView(LoginRequiredMixin, CreateView):
    model = TrainerRating
    form_class = TrainerRatingForm
    template_name = 'workouts/submit_trainer_rating.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trainer = get_object_or_404(settings.AUTH_USER_MODEL, pk=self.kwargs['trainer_id'])
        context['trainer'] = trainer
        return context

    def form_valid(self, form):
        trainer = get_object_or_404(settings.AUTH_USER_MODEL, pk=self.kwargs['trainer_id'])
        form.instance.trainer = trainer
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('trainer_dashboard')
