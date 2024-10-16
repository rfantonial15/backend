from django.db import models
from django.utils import timezone

class Alert(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly define an auto-incrementing ID
    subject = models.CharField(max_length=255)
    message = models.TextField()
    image = models.ImageField(upload_to='alerts/', null=True, blank=True)
    files = models.FileField(upload_to='files/', null=True, blank=True)
    links = models.JSONField(default=list, blank=True)
    time = models.DateTimeField(default=timezone.now)  # Set to current time when alert is created

    def __str__(self):
        return self.subject
