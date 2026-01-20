from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg


# ---------- USER ----------
class UserProfile(AbstractUser):
    ROLE_CHOICES = (
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')
    phone_number = PhoneNumberField(unique=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.username
class City(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


# ---------- PROPERTY ----------
class Property(models.Model):
    PROPERTY_TYPE_CHOICES = (
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('studio', 'Studio'),
    )

    RULES_CHOICES = (
        ('no_smoking', 'No smoking'),
        ('pets_allowed', 'Pets allowed'),
    )

    title = models.CharField(max_length=255)


    description = models.TextField()
    price_per_night = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="property_city")

    address = models.CharField(max_length=255)
    property_type = models.CharField(
        max_length=20, choices=PROPERTY_TYPE_CHOICES
    )
    rules = models.CharField(
        max_length=50, choices=RULES_CHOICES, blank=True
    )
    max_guests = models.PositiveIntegerField()
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    owner = models.ForeignKey( UserProfile, on_delete=models.CASCADE, related_name='properties')
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.title


class PropertyImage(models.Model):
    property = models.ForeignKey( Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/')
    def __str__(self):
        return f"Image for {self.property.title}"


class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    )
    property = models.ForeignKey( Property, on_delete=models.CASCADE )
    guest = models.ForeignKey( UserProfile, on_delete=models.CASCADE )
    check_in = models.DateField()
    check_out = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.property} - {self.guest}"


class Review(models.Model):
    property = models.ForeignKey( Property, on_delete=models.CASCADE , related_name='reviews')
    guest = models.ForeignKey( UserProfile, on_delete=models.CASCADE )
    guest = models.ForeignKey( UserProfile, on_delete=models.CASCADE )
    rating = models.PositiveSmallIntegerField( validators=[MinValueValidator(1), MaxValueValidator(5)] )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def average_rating(self):
        result = self.reviews.aggregate(avg=Avg('rating'))  # reviews — related_name от Review
        return result['avg'] or 0
    def __str__(self):
        return f"{self.rating}/5"
