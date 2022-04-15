from django.urls import include, path
from rest_framework.routers import DefaultRouter

api_routes = DefaultRouter()

urlpatterns = [
    path("", include(api_routes.urls)),
]