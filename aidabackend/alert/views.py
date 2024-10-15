from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Alert
from .serializers import AlertSerializer

class AlertListCreateView(APIView):
    # GET method for fetching all alerts
    def get(self, request, *args, **kwargs):
        subject = request.query_params.get('subject', None)
        if subject:
            alerts = Alert.objects.filter(subject=subject)
            if alerts.exists():
                serializer = AlertSerializer(alerts, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"error": "Alert not found"}, status=status.HTTP_404_NOT_FOUND)
        alerts = Alert.objects.all()
        serializer = AlertSerializer(alerts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # POST method for creating a new alert
    def post(self, request, *args, **kwargs):
        serializer = AlertSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
