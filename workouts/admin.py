from django.contrib import admin
from .models import Workout, UserWorkoutSignup, UserWorkoutHistory

admin.site.register(Workout)
admin.site.register(UserWorkoutSignup)
admin.site.register(UserWorkoutHistory)