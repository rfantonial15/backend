import random
from django.db import models

class User(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)  # Store hashed passwords
    phone = models.CharField(max_length=15, blank=True, null=True)
    barangay = models.CharField(max_length=100, blank=True, null=True)
    isadmin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)  # Verification status
    verification_code = models.CharField(max_length=5, blank=True, null=True)  # 5-digit code

    def generate_verification_code(self):
        """Generate and save a new 5-digit verification code."""
        self.verification_code = f"{random.randint(10000, 99999)}"  # Generates a 5-digit random code
        self.save(update_fields=['verification_code'])  # Only update the verification_code field

    def __str__(self):
        return self.username
