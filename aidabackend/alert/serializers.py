from rest_framework import serializers
from .models import Alert

class AlertSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField(format='%I:%M %p', read_only=True)  # Read-only field, auto-generated

    class Meta:
        model = Alert
        fields = ['id', 'subject', 'message', 'image', 'files', 'links', 'time']  # Include the time field, but it's read-only
