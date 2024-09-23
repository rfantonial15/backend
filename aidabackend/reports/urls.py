from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReportViewSet, AlertViewSet

router = DefaultRouter()
router.register(r'reports', ReportViewSet)
router.register(r'alerts', AlertViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
