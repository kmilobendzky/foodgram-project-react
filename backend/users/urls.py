from django.urls import include, path

urlpatterns = [
    path('', include('djoser.urls')),
    path('token/', include('djoser.urls.')),
]