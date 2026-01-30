from django.urls import path
from .views import get_data, get_trailer

urlpatterns = [
    path("movie/",get_data),
    path("movie/trailer/",get_trailer)
]