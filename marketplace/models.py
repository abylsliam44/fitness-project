from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class ProductManager(models.Manager):
    def active(self):
        today = timezone.now().date()
        return self.filter(is_active=True).exclude(expires_at__lt=today)


class Product(models.Model):
    PRODUCT_TYPE_CHOICES = [
        ('product', 'Product'),
        ('service', 'Service'),
    ]

    CONDITION_CHOICES = [
        ('new', 'New'),
        ('like_new', 'Like New'),
        ('used', 'Used'),
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('sold', 'Sold'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=PRODUCT_TYPE_CHOICES, default='product')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    slug = models.SlugField(unique=True, blank=True)

    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='new')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    expires_at = models.DateField(null=True, blank=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='listings'
    )

    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        if not self.expires_at:
            self.expires_at = timezone.now().date() + timedelta(days=30)

        super().save(*args, **kwargs)

    def is_expired(self):
        return self.expires_at and timezone.now().date() > self.expires_at

    def __str__(self):
        return f"{self.title} by {self.owner.username}"
    
    objects = ProductManager()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.product.title}"
    

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} ➝ {self.product.title}"
    

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    reply = models.TextField(blank=True, null=True)
    replied_at = models.DateTimeField(blank=True, null=True)

    def is_author_reply(self):
        return self.reply is not None

    def __str__(self):
        return f"Comment by {self.author.username} on {self.product.title}"


