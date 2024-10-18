from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = (
        'date_time',    
        'incident_type', 
        'victim_name',
        'victim_age',
        'victim_sex',
        'landmark',
        'city',
    )
    search_fields = ('victim_name', 'incident_type') 