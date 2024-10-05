# alert/urls.py

from django.urls import path
from .views import AlertListCreateView

urlpatterns = [
    path('alerts/', AlertListCreateView.as_view(), name='alert-list-create'),  # This route handles GET and POST requests
]
