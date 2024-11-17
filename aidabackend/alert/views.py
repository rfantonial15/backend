from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Alert
from .serializers import AlertSerializer
from rest_framework.permissions import AllowAny

class AlertListCreateView(APIView):
    permission_classes = [AllowAny]
    # GET method for fetching all alerts or a single alert by id
    def get(self, request, id=None, *args, **kwargs):
        if id:  # If id is provided, fetch specific alert
            try:
                alert = Alert.objects.get(id=id)
                serializer = AlertSerializer(alert)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Alert.DoesNotExist:
                return Response({"error": "Alert not found"}, status=status.HTTP_404_NOT_FOUND)
        else:  # If no id, return all alerts
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
