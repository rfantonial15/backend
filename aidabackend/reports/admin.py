from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'incident', 'victim_name', 'age', 'sex', 'address')
    search_fields = ('victim_name', 'incident')
