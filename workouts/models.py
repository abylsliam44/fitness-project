from django.db import models
from django.conf import settings
from django.utils.text import slugify


class WorkoutCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Workout(models.Model):
    title        = models.CharField(max_length=200)
    description  = models.TextField()
    category     = models.ForeignKey(
        WorkoutCategory,
        related_name='workouts',
        on_delete=models.CASCADE
    )
    duration     = models.PositiveIntegerField(help_text="Duration (minutes)")
    capacity     = models.PositiveIntegerField(default=20, help_text="Max participants")
    video_url    = models.URLField(blank=True, null=True)
    image        = models.ImageField(upload_to='workout_images/', blank=True, null=True)
    trainer      = models.ForeignKey(
                      settings.AUTH_USER_MODEL,
                      related_name='workouts',
                      on_delete=models.CASCADE
                   )
    slug = models.SlugField(unique=True, blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def available_slots(self) -> int:
        return self.capacity - self.signups.count()

    def is_user_enrolled(self, user) -> bool:
        return user.is_authenticated and self.signups.filter(user=user).exists()

    def __str__(self):
        return self.title


class UserWorkoutSignup(models.Model):
    user         = models.ForeignKey(
                       settings.AUTH_USER_MODEL,
                       related_name='workout_signups',
                       on_delete=models.CASCADE
                   )
    workout      = models.ForeignKey(
                       Workout,
                       related_name='signups',
                       on_delete=models.CASCADE
                   )
    signed_up_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'workout')

    def __str__(self):
        return f'{self.user.username} → {self.workout.title}'


class UserWorkoutHistory(models.Model):
    user         = models.ForeignKey(
                       settings.AUTH_USER_MODEL,
                       related_name='workout_history',
                       on_delete=models.CASCADE
                   )
    workout      = models.ForeignKey(Workout, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)
    status       = models.CharField(max_length=50, default="completed")
    repetitions  = models.IntegerField(default=0)
    weight       = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} — {self.workout.title} ({self.status})'


class WorkoutReview(models.Model):
    workout    = models.ForeignKey(
                    Workout, related_name='reviews',
                    on_delete=models.CASCADE
                )
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text       = models.TextField()
    rating     = models.IntegerField(
                    choices=[(i, f'{i} star') for i in range(1,6)],
                    default=1
                )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user.username} for {self.workout.title}'


class WorkoutPlan(models.Model):
    user      = models.ForeignKey(
                    settings.AUTH_USER_MODEL,
                    related_name='workout_plans',
                    on_delete=models.CASCADE
                )
    title     = models.CharField(max_length=200)
    description = models.TextField()
    start_date  = models.DateField()
    end_date    = models.DateField()
    workouts    = models.ManyToManyField(Workout)

    def __str__(self):
        return self.title


class GroupWorkout(models.Model):
    workout           = models.ForeignKey(Workout, on_delete=models.CASCADE)
    scheduled_at      = models.DateTimeField()
    max_participants  = models.PositiveIntegerField(default=10)
    participants      = models.ManyToManyField(
                            settings.AUTH_USER_MODEL,
                            through='GroupWorkoutParticipant'
                        )

    def available_slots(self) -> int:
        return self.max_participants - self.participants.count()

    def __str__(self):
        return f'{self.workout.title} @ {self.scheduled_at}'


class GroupWorkoutParticipant(models.Model):
    group_workout = models.ForeignKey(GroupWorkout, on_delete=models.CASCADE)
    user          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    signed_up_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('group_workout', 'user')

    def __str__(self):
        return f'{self.user.username} in {self.group_workout}'


class TrainerRating(models.Model):
    trainer    = models.ForeignKey(
                    settings.AUTH_USER_MODEL,
                    related_name='trainer_ratings',
                    on_delete=models.CASCADE
                 )
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating     = models.IntegerField(
                    choices=[(i, f'{i} star') for i in range(1,6)],
                    default=1
                 )
    text       = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Rating for {self.trainer.username} by {self.user.username}'


class Notification(models.Model):
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read    = models.BooleanField(default=False)

    def __str__(self):
        return f'Notification to {self.user.username}'
