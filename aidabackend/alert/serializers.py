from datetime import datetime
from rest_framework import serializers
from .models import Alert

class AlertSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField(format='%B %d, %Y - %I:%M:%S %p', default=datetime.now)

    class Meta:
        model = Alert
        fields = ['id', 'subject', 'message', 'image', 'files', 'links', 'time']
