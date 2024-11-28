from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.core.exceptions import ValidationError
import boto3
import uuid
from .models import Alert
from .serializers import AlertSerializer
from rest_framework.permissions import AllowAny


class AlertListCreateView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id=None):
        """
        Fetch all alerts or a specific alert by ID.
        """
        if id:
            try:
                alert = Alert.objects.get(id=id)
                serializer = AlertSerializer(alert)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Alert.DoesNotExist:
                return Response({"error": "Alert not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            alerts = Alert.objects.all().order_by('-time')  # Fetch all alerts, ordered by time
            serializer = AlertSerializer(alerts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new alert with optional image, files, and links.
        """
        try:
            subject = request.POST.get("subject", "")
            message = request.POST.get("message", "")
            recipients = request.POST.get("recipients", "[]")
            links = request.POST.get("links", "[]")

            if not subject or not message or recipients == "[]":
                return Response(
                    {"error": "Subject, message, and recipients are required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Handle S3 uploads for image
            image_url = None
            if "image" in request.FILES:
                image = request.FILES["image"]
                image_url = self.upload_to_s3(image, "alert_images/")

            # Handle S3 uploads for files
            file_urls = []
            for key in request.FILES:
                if key.startswith("file_"):
                    file = request.FILES[key]
                    file_url = self.upload_to_s3(file, "alert_files/")
                    file_urls.append(file_url)

            # Save alert data
            alert_data = {
                "subject": subject,
                "message": message,
                "image": image_url,
                "files": file_urls,
                "links": links,
            }
            serializer = AlertSerializer(data=alert_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def upload_to_s3(self, file, folder):
        """
        Upload a file to S3 and return its URL.
        """
        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME,
            )
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            unique_filename = f"{folder}{uuid.uuid4()}_{file.name}"
            s3_client.upload_fileobj(
                file,
                bucket_name,
                unique_filename,
                ExtraArgs={'ContentType': file.content_type}
            )
            return f"https://{bucket_name}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{unique_filename}"
        except Exception as e:
            raise ValidationError(f"Failed to upload to S3: {str(e)}")
