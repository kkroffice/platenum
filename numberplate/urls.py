from django.urls import path
from .views import save_trespassing_info

urlpatterns = [
    path('api/save-trespassing-info/', save_trespassing_info, name='save_trespassing_info'),
]
