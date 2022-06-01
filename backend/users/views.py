import rest_framework.permissions as permissions
from api.pagination import CustomPaginationClass
from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Follow, User
from .serializers import FollowSerializer


class FollowViewSet(APIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination = CustomPaginationClass

    def post(self, request, pk):
        user = self.request.user
        following = get_object_or_404(User, id=pk)
        if user == following:
            return Response(
                {'error': 'Нельзя подписаться на самого себя!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if Follow.objects.filter(
                user=user,
                following=following
        ).exists():
            return Response(
                {'error': 'Вы уже подписаны на пользователя!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        subscription = Follow.objects.create(
            user=user,
            following=following)
        serializer = FollowSerializer(
            subscription,
            context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        user = self.request.user
        following = get_object_or_404(User, id=pk)
        subscription = Follow.objects.filter(
            user=user,
            following=following)
        if subscription.exists():
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class FollowListView(ListAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPaginationClass

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(user=user)
