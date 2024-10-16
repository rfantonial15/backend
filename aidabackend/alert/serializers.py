from rest_framework import serializers
from .models import Alert
from datetime import datetime

class AlertSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField(format='%I:%M %p', read_only=True)
    timeDate = serializers.DateTimeField(format='%B %d, %Y - %I:%M:%S %p', default=datetime.now)

    class Meta:
        model = Alert
        fields = ['id', 'subject', 'message', 'image', 'files', 'links', 'time', 'timeDate']
