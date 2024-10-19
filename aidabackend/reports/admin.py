from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = (
        'reporter_name',   # Add reporter_name here
        'date_time',
        'incident_type',
        'victim_name',
        'victim_age',
        'victim_sex',
        'landmark',
        'city',
    )
    search_fields = ('reporter_name', 'victim_name', 'incident_type')  # Add reporter_name to search fields
