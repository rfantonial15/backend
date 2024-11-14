from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReportViewSet, detect_incident
from django.conf.urls.static import static
from django.conf import settings

# Register the ReportViewSet with a router
router = DefaultRouter()
router.register(r'reports', ReportViewSet, basename='report')  # Adding basename for clarity

urlpatterns = [
    path('', include(router.urls)),  # Includes all routes for ReportViewSet
    path('detect-incident/', detect_incident, name='detect_incident'),  # Direct path for detect-incident
]

# Serve media files in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
