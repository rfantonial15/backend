# alert/views.py

from rest_framework import generics
from .models import Alert
from .serializers import AlertSerializer
from rest_framework.permissions import IsAuthenticated

class AlertListCreateView(generics.ListCreateAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]  # Ensure that the user is authenticated
