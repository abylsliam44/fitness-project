from django.db import models
from django.conf import settings
from django.utils.text import slugify


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
    trainer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='workouts', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class UserWorkoutSignup(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='workout_signups')
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    signed_up_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} signed up for {self.workout.title}"


class UserWorkoutHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='workout_history')
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="completed")
    repetitions = models.IntegerField(default=0)  # Количество повторений (если применимо)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Вес (если применимо)

    def __str__(self):
        return f"{self.user.username} - {self.workout.title} - {self.status}"


class WorkoutReview(models.Model):
    workout = models.ForeignKey(Workout, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(default=1, choices=[(1, '1 star'), (2, '2 stars'), (3, '3 stars'), (4, '4 stars'), (5, '5 stars')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.workout.title} by {self.user.username}"


class WorkoutPlan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='workout_plans')
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    workouts = models.ManyToManyField(Workout)

    def __str__(self):
        return self.title


class GroupWorkout(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    scheduled_at = models.DateTimeField()
    max_participants = models.IntegerField(default=10)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, through='GroupWorkoutParticipant')

    def __str__(self):
        return f"{self.workout.title} - {self.scheduled_at}"


class GroupWorkoutParticipant(models.Model):
    group_workout = models.ForeignKey(GroupWorkout, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    signed_up_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} signed up for {self.group_workout.workout.title}"


class TrainerRating(models.Model):
    trainer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='trainer_ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1, choices=[(1, '1 star'), (2, '2 stars'), (3, '3 stars'), (4, '4 stars'), (5, '5 stars')])
    text = models.TextField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating for {self.trainer.username} by {self.user.username}"


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}"
