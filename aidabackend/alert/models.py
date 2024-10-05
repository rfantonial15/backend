# alert/models.py

from django.db import models
from django.conf import settings  # Import settings to reference the User model

class Alert(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Link to the User model
    subject = models.CharField(max_length=100)
    message = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)  # Automatically set to now when created

    def __str__(self):
        return f'Alert from {self.user.username}: {self.subject}'
