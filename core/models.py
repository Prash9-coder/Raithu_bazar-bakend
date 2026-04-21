from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('seller', 'Seller'),
        ('buyer', 'Buyer'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')
    mobile_number = models.CharField(max_length=15, unique=True)
    village = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    full_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.full_name} ({self.role})"

class CowListing(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('sold', 'Sold'),
    )
    
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    tag_name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    milk_per_day = models.DecimalField(max_digits=5, decimal_places=2, help_text="Liters per day")
    health_condition = models.TextField()
    vaccination_details = models.TextField()
    pregnant_status = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    negotiable = models.BooleanField(default=True)
    village = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tag_name} - {self.breed}"

class CowImage(models.Model):
    cow = models.ForeignKey(CowListing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='cow_images/') # Cloudinary will handle this via storage backend
    created_at = models.DateTimeField(auto_now_add=True)

class Inquiry(models.Model):
    cow = models.ForeignKey(CowListing, on_delete=models.CASCADE, related_name='inquiries')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_inquiries')
    name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry from {self.name} for {self.cow.tag_name}"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    cow = models.ForeignKey(CowListing, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'cow')
