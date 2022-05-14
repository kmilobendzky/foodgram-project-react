from django.urls import include, path

from .views import FollowListView, FollowViewSet

urlpatterns = [
    path(
        'users/subscriptions/',
        FollowListView.as_view(),
        name='subscriptions'
    ),
    path(
        'users/<int:pk>/subscribe/',
        FollowViewSet.as_view(),
        name='subscribe'
    ),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
