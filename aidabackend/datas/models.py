import random

from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, firstname, lastname, email, username, phone, barangay, password=None, **extra_fields):
        if not firstname and not lastname and not email and not username and not phone and not barangay:
            raise ValueError("All fields must be set")

        user = self.model(
            firstname=firstname, 
            lastname=lastname, 
            email=email, 
            username=username, 
            phone=phone, 
            barangay=barangay,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, firstname, lastname, email, username, phone, barangay, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("isadmin", True)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('isadmin') is not True:
            raise ValueError('Superuser must have isadmin=True.')
        if extra_fields.get('is_verified') is not True:
            raise ValueError('Superuser must have is_verified=True.')

        return self.create_user(firstname, lastname, email, username, phone, barangay, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)  # Store hashed passwords
    phone = models.CharField(max_length=15, blank=True, null=True)
    barangay = models.CharField(max_length=100, blank=True, null=True)
    isadmin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)  # Verification status
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    verification_code = models.CharField(max_length=5, blank=True, null=True)  # 5-digit code

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["firstname", "lastname", "username", "phone", "barangay"]

    def generate_verification_code(self):
        """Generate and save a new 5-digit verification code."""
        self.verification_code = f"{random.randint(10000, 99999)}"  # Generates a 5-digit random code
        self.save(update_fields=['verification_code'])  # Only update the verification_code field

    def __str__(self):
        return self.username
