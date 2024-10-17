from rest_framework import viewsets
from rest_framework.response import Response
from .models import Report
from .serializers import ReportSerializer

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        # We expect a PATCH request to include 'remarks' in the request data.
        if 'remarks' in request.data:
            instance.remarks = request.data['remarks']  # Toggle remarks based on frontend request
            instance.save()
            return Response(self.get_serializer(instance).data)
        return Response({"error": "Invalid request"}, status=400)
