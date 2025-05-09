from django.db import models
from django.conf import settings

class Workout(models.Model):
    CATEGORY_CHOICES = [
        ('strength', 'Strength'),
        ('cardio', 'Cardio'),
        ('stretch', 'Stretch'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50)
    duration = models.IntegerField(help_text="Duration in minutes")
    video_url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='workout_images/', blank=True, null=True)
    trainer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='trainings', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class UserWorkoutSignup(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    signed_up_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} signed up for {self.workout.title}"


class UserWorkoutHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="completed")

    def __str__(self):
        return f"{self.user.username} - {self.workout.title} - {self.status}"
