from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Report
from .serializers import ReportSerializer

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        if 'remarks' in request.data:
            instance.remarks = request.data['remarks']
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
