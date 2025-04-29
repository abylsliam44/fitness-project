from django.urls import path
from .views import (
    WorkoutListView,
    SignUpForWorkoutView,
    UserWorkoutHistoryView,
    TrainerDashboardView,
    WorkoutCreateView,
    WorkoutReviewCreateView,
    WorkoutPlanCreateView,
    GroupWorkoutCreateView,
    TrainerRatingCreateView
)

urlpatterns = [
    path('', WorkoutListView.as_view(), name='workouts_list'),  
    path('signup/<slug:slug>/', SignUpForWorkoutView.as_view(), name='sign_up_for_workout'),  
    path('history/', UserWorkoutHistoryView.as_view(), name='user_workout_history'),  
    path('trainer/dashboard/', TrainerDashboardView.as_view(), name='trainer_dashboard'),  
    path('trainer/create/', WorkoutCreateView.as_view(), name='workout_create'),
    path('workouts/review/<slug:slug>/', WorkoutReviewCreateView.as_view(), name='add_review'),
    path('workouts/plan/create/', WorkoutPlanCreateView.as_view(), name='create_workout_plan'),
    path('workouts/group/create/', GroupWorkoutCreateView.as_view(), name='create_group_workout'),
    path('trainers/rate/<int:trainer_id>/', TrainerRatingCreateView.as_view(), name='rate_trainer'),
]
