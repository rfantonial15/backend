from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Report
from .serializers import ReportSerializer
from django.http import JsonResponse
from inference_sdk import InferenceHTTPClient
from django.views.decorators.csrf import csrf_exempt
import os
import tempfile
import uuid
from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [AllowAny]  # Allow anyone to create reports
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        # Extract data manually from the request to create a Report instance
        report = Report(
            reporter_name=data.get('reporter_name', 'Unknown Reporter'),
            image_url=data.get('image_url', ''),
            incident_type=data.get('incident_type', 'No incident detected'),
            latitude=float(data.get('latitude', 0.0)),
            longitude=float(data.get('longitude', 0.0)),
            date_time=data.get('date_time'),
            landmark=data.get('landmark', ''),
            barangay=data.get('barangay', ''),
            city=data.get('city', ''),
            victim_name=data.get('victim_name', ''),
            victim_age=int(data.get('victim_age', 0)),
            victim_sex=data.get('victim_sex', ''),
            spot_report=data.get('spot_report', ''),
            duty=data.get('duty', ''),
            remarks=data.get('remarks', 'Pending')
        )

        # Save the report to the database
        report.save()

        # Serialize the newly created report to return it in the response
        serializer = self.get_serializer(report)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if 'remarks' in request.data:
            instance.remarks = request.data['remarks']
            instance.save(update_fields=['remarks'])  # Only update the 'remarks' field
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="lvRVpI8zrOHMnk87ZLAC"
)

@csrf_exempt
def detect_incident(request):
    if request.method == "POST" and request.FILES.get("image"):
        # Generate a unique filename to avoid conflicts
        filename = f"{uuid.uuid4()}.jpg"
        media_path = os.path.join(settings.MEDIA_ROOT, 'incident_images', filename)
        os.makedirs(os.path.dirname(media_path), exist_ok=True)

        # Save the uploaded image to the media directory
        with open(media_path, 'wb') as media_file:
            media_file.write(request.FILES["image"].read())

        try:
            # Perform incident detection
            result = CLIENT.infer(media_path, model_id="incident_classification/13")
            predictions = result.get("predictions", [])
            detected_class = predictions[0]["class"] if predictions else None

            # Return detection information and the media URL
            image_url = f"{settings.MEDIA_URL}incident_images/{filename}"
            return JsonResponse({
                "incident_type": detected_class,
                "captured_image": image_url  # Return the URL to the image
            }, safe=False)
        except Exception as e:
            os.remove(media_path)
            print(f"Error during inference: {e}")
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)
