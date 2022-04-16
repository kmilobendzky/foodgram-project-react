from django.shortcuts import render
from api.models import Tag, Ingredient
from api.serializers import TagSerializer, IngredientSerializer
import rest_framework.permissions as permissions


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = None
    search_fields = ('name')


class IngredientViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = None

    def get_queryset(self):
        post_id = Ingredient.objects.all()
        post = get_object_or_404(Post, pk=post_id)
        return post.comments.all()

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужих комментариев запрещено!')
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужих комментариев запрещено!')
        return super().perform_destroy(instance)

class RecipeViewSet()