from django.urls import path
from .views import (
    WorkoutListView,
    SignUpForWorkoutView,
    UserWorkoutHistoryView,
    TrainerDashboardView,
    WorkoutCreateView
)

urlpatterns = [
    path('', WorkoutListView.as_view(), name='workouts_list'),  
    path('signup/<slug:slug>/', SignUpForWorkoutView.as_view(), name='sign_up_for_workout'),  
    path('history/', UserWorkoutHistoryView.as_view(), name='user_workout_history'),  
    path('trainer/dashboard/', TrainerDashboardView.as_view(), name='trainer_dashboard'),  
    path('trainer/create/', WorkoutCreateView.as_view(), name='workout_create'),  
]
