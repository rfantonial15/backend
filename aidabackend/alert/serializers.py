# alert/serializers.py

from rest_framework import serializers
from .models import Alert

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ['id', 'user', 'subject', 'message', 'date_time']
        read_only_fields = ['user', 'date_time']  # Optionally, you might want to restrict these fields
