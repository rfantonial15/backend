from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('datas.urls')),
    path('api/', include('reports.urls')),
    path('api/', include('alert.urls')),  # Ensure this line is correct
]
