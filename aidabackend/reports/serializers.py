from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = [
            'image_url',
            'incident_type',
            'longitude',
            'latitude',
            'date_time',
            'landmark',
            'barangay',
            'city',
            'victim_name',
            'victim_age',
            'victim_sex',
            'spot_report',
            'duty',
            'remarks',
        ]