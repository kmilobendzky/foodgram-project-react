from django.shortcuts import render
from api.models import Tag, Ingredient, Recipe
from api.serializers import (
    TagSerializer, 
    IngredientSerializer, 
    RecipeCreationSerializer,
    RecipeListSerializer)
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
        queryset = Ingredient.objects.all()
        return queryset

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeListSerializer
    permission_classes= (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeListSerializer
        else:
            return RecipeCreationSerializer