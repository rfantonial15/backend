from django.urls import path
from .views import AlertListCreateView

urlpatterns = [
    path('alerts/', AlertListCreateView.as_view(), name='alert-list-create'),
    path('alerts/', AlertListCreateView.as_view(), name='alert-list-create'),
    path('alerts/<int:id>/', AlertListCreateView.as_view(), name='alert-detail'),
]
