from django.db import models
from django.utils import timezone

class Alert(models.Model):
    subject = models.CharField(max_length=255)
    message = models.TextField()
    image = models.URLField(null=True, blank=True)  # Store S3 URL for image
    files = models.JSONField(null=True, blank=True, default=list)  # Handle empty or missing files
    links = models.JSONField(null=True, blank=True, default=list)  # Handle empty or missing links
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.subject
