from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('datas.urls')),  # Include your app's URLs
    path('api/', include('reports.urls')),  # Include reports app URLs
]
