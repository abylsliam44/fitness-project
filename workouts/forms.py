from django import forms
from .models import Workout, WorkoutReview, WorkoutPlan, GroupWorkout, TrainerRating

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['title', 'description', 'category', 'duration', 'video_url', 'image']

class WorkoutReviewForm(forms.ModelForm):
    class Meta:
        model = WorkoutReview
        fields = ['text', 'rating']

class WorkoutPlanForm(forms.ModelForm):
    class Meta:
        model = WorkoutPlan
        fields = ['title', 'description', 'start_date', 'end_date', 'workouts']
    

class GroupWorkoutForm(forms.ModelForm):
    class Meta:
        model = GroupWorkout
        fields = ['workout', 'scheduled_at', 'max_participants']
        widgets = {
            'scheduled_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class TrainerRatingForm(forms.ModelForm):
    class Meta:
        model = TrainerRating
        fields = ['rating', 'text']