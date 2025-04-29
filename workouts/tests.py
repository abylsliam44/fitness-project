import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Workout
from django.test import Client
from views import UserWorkoutSignup

@pytest.mark.django_db
def test_sign_up_for_workout_view():
    user = get_user_model().objects.create_user(username="testuser", password="password123")
    workout = Workout.objects.create(name="Yoga", description="Yoga session", slug="yoga-slug")

    client = Client()
    client.login(username="testuser", password="password123")

    response = client.get(reverse('sign_up_for_workout', kwargs={'slug': workout.slug}))

    assert response.status_code == 200
    assert workout.name in str(response.content)

    response_post = client.post(reverse('sign_up_for_workout', kwargs={'slug': workout.slug}), data={'workout': workout.id})
    
    assert response_post.status_code == 302  
    assert UserWorkoutSignup.objects.filter(user=user, workout=workout).exists() 
