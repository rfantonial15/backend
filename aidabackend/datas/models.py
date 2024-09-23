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

    def __str__(self):
        return self.username

