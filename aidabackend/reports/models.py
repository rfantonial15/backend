from django.db import models

class Report(models.Model):
    date = models.DateField()
    time = models.TimeField()
    incident = models.CharField(max_length=255)
    victim_name = models.CharField(max_length=255)
    age = models.IntegerField()
    sex = models.CharField(max_length=10)
    address = models.CharField(max_length=255)
    spot = models.CharField(max_length=255)
    duty = models.CharField(max_length=255)
    remarks = models.TextField()

    def __str__(self):
        return f"{self.incident} - {self.victim_name}"

class Alert(models.Model):
    subject = models.CharField(max_length=255)
    message = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject