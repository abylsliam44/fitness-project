from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.contrib.auth.hashers import make_password

# User roles
USER_ROLES = (
    ('user', 'Regular User'),
    ('trainer', 'Trainer'),
    ('admin', 'Administrator'),
)

# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        """Creates and returns a regular user"""
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)

        if password:  
            extra_fields['password'] = make_password(password)  

        if extra_fields.get('role') == 'admin':
            extra_fields.setdefault('is_staff', True)
            extra_fields.setdefault('is_superuser', True)
        elif extra_fields.get('role') == 'trainer':
            extra_fields.setdefault('is_staff', True)

        user = self.model(email=email, username=username, **extra_fields)
        user.save(using=self._db)
        return user



# Custom User Model
class User(AbstractUser):
    role = models.CharField(max_length=10, choices=USER_ROLES, default='user')
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    is_staff = models.BooleanField(default=False)  
    is_superuser = models.BooleanField(default=False)  

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_groups",  
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions",  
        blank=True
    )

    def clean(self):
        """Custom validation for User fields"""
        if not self.username:
            raise ValidationError("Username is required.")
        if self.username and len(self.username) < 3:
            raise ValidationError("Username must be at least 3 characters long.")
        if not self.email:
            raise ValidationError("Email is required.")
        if self.email and '@' not in self.email:
            raise ValidationError("Please enter a valid email address.")
        
        # Присвоение флагов в зависимости от роли
        if self.role == 'admin':
            self.is_staff = True
            self.is_superuser = True
        elif self.role == 'trainer':
            self.is_staff = True


    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

# Profile Model
class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    birth_date = models.DateField(blank=True, null=True)  
    weight = models.FloatField(blank=True, null=True)  
    height = models.FloatField(blank=True, null=True)  
    goal = models.CharField(max_length=255, blank=True, null=True) 
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])]
    )
    slug = models.SlugField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=[('male', 'Male'), ('female', 'Female')],
        null=True,
        blank=True
    )
    
    def age(self):
        if self.birth_date:
            from datetime import date
            today = date.today()
            return today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
            )
        return None

    age.short_description = "Age"
    
    def bmi(self):
        if self.weight and self.height:
            return round(self.weight / ((self.height / 100) ** 2), 2)
        return None

    bmi.short_description = "BMI (Body Mass Index)"
