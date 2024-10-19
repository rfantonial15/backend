from django.db import models
from django.utils import timezone

class Report(models.Model):
    id = models.AutoField(primary_key=True)
    reporter_name = models.CharField(max_length=255, default='Unknown Reporter')
    image_url = models.URLField(default='')
    incident_type = models.CharField(max_length=255)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0) 
    date_time = models.DateTimeField(default=timezone.now)
    landmark = models.CharField(max_length=255)
    barangay = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    victim_name = models.CharField(max_length=255)
    victim_age = models.IntegerField()
    victim_sex = models.CharField(max_length=10)
    spot_report = models.TextField()
    duty = models.CharField(max_length=255)
    remarks = models.CharField(
        max_length=10,
        choices=[('Pending', 'Pending'), ('Done', 'Done')],
        default='Pending'
    )

    def __str__(self):
        return f"{self.incident_type} - {self.victim_name}"
