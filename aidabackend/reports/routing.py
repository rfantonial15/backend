from django.urls import path
from .consumers import ReportNotificationConsumer

websocket_urlpatterns = [
    path('ws/reports/', ReportNotificationConsumer.as_asgi()),
]
