import boto3
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
from botocore.exceptions import NoCredentialsError
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [AllowAny]  # Allow anyone to create and update reports
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
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
        report.save()

        # Only send notifications during report creation
        try:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "reports",
                {
                    "type": "send_notification",
                    "report": {
                        "reporter_name": report.reporter_name,
                        "incident_type": report.incident_type,
                        "image_url": report.image_url,
                        "barangay": report.barangay,
                        "city": report.city,
                        "remarks": report.remarks,
                        "latitude": report.latitude,
                        "longitude": report.longitude,
                        "date_time": str(report.date_time),
                    },
                },
            )
        except Exception as e:
            print(f"Error sending WebSocket notification: {e}")

        serializer = self.get_serializer(report)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Prevent notifications during partial updates
        for field, value in request.data.items():
            if hasattr(instance, field):
                setattr(instance, field, value)
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def update(self, request, *args, **kwargs):
        # This handles full updates (all fields must be sent in the request)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        instance.save() 

        return Response(serializer.data, status=status.HTTP_200_OK)
    
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="lvRVpI8zrOHMnk87ZLAC"
)

@csrf_exempt
def detect_incident(request):
    if request.method == "POST" and request.FILES.get("image"):
        try:
            print("Starting detect_incident function...")

            # Retrieve the uploaded file
            uploaded_file = request.FILES["image"]
            print("File received:", uploaded_file.name)

            # Perform incident detection directly on the file
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                for chunk in uploaded_file.chunks():
                    temp_file.write(chunk)
                temp_file_path = temp_file.name

            print("Temporary file path:", temp_file_path)

            # Perform incident detection using the local file path
            result = CLIENT.infer(temp_file_path, model_id="incident_classification/13")
            print("Inference result received:", result)

            # Extract predictions
            predictions = result.get("predictions", [])
            detected_class = predictions[0]["class"] if predictions else "Unknown"
            print("Detected class:", detected_class)

            # If no valid incident is detected, do not upload the image
            if detected_class == "Unknown":
                print("No valid incident detected. Skipping S3 upload.")
                return JsonResponse({
                    "incident_type": "Unknown",
                    "captured_image": None  # No image URL since not uploaded
                }, safe=False)

            # Generate a unique filename for the valid incident
            unique_filename = f"incident_images/{uuid.uuid4()}.jpg"
            print("Generated unique filename:", unique_filename)

            # Upload file to S3
            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME
            )
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME

            with open(temp_file_path, "rb") as file_obj:
                s3_client.upload_fileobj(
                    file_obj,
                    bucket_name,
                    unique_filename,
                    ExtraArgs={'ContentType': uploaded_file.content_type}
                )
            print("File uploaded to S3")

            # Generate the public URL for the uploaded file
            image_url = f"https://{bucket_name}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{unique_filename}"
            print("S3 URL of uploaded file:", image_url)

            # Return the response
            return JsonResponse({
                "incident_type": detected_class,
                "captured_image": image_url  # Return the public S3 URL
            }, safe=False)

        except NoCredentialsError as e:
            print("S3 credentials error:", e)
            return JsonResponse({"error": "S3 credentials not found. Check your AWS settings."}, status=500)
        except Exception as e:
            print("Error occurred:", str(e))
            return JsonResponse({"error": str(e)}, status=500)
        finally:
            if temp_file_path:
                os.remove(temp_file_path)  # Clean up the temporary file

    print("Invalid request received.")
    return JsonResponse({"error": "Invalid request. Please provide an image."}, status=400)


@csrf_exempt
def upload_image(request):
    if request.method == "POST" and request.FILES.get("image"):
        try:
            print("Starting upload_image function...")

            # Retrieve the uploaded file
            uploaded_file = request.FILES["image"]
            print("File received:", uploaded_file.name)

            # Generate a unique filename
            unique_filename = f"incident_images/{uuid.uuid4()}.jpg"
            print("Generated unique filename:", unique_filename)

            # Upload file to S3
            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME
            )
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME

            s3_client.upload_fileobj(
                uploaded_file,
                bucket_name,
                unique_filename,
                ExtraArgs={'ContentType': uploaded_file.content_type}
            )
            print("File uploaded to S3")

            # Generate the public URL for the uploaded file
            image_url = f"https://{bucket_name}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{unique_filename}"
            print("S3 URL of uploaded file:", image_url)

            # Return the S3 URL of the uploaded image
            return JsonResponse({"image_url": image_url}, status=200)

        except NoCredentialsError as e:
            print("S3 credentials error:", e)
            return JsonResponse({"error": "S3 credentials not found. Check your AWS settings."}, status=500)
        except Exception as e:
            print("Error occurred:", str(e))
            return JsonResponse({"error": str(e)}, status=500)

    print("Invalid request received.")
    return JsonResponse({"error": "Invalid request. Please provide an image."}, status=400)