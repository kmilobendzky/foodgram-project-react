from django.shortcuts import render
from api.models import Tag, Ingredient, Recipe, Favourite, ShoppingCart, IngredientAmount
from api.serializers import (
    TagSerializer, 
    IngredientSerializer, 
    RecipeCreationSerializer,
    RecipeListSerializer)
from rest_framework import filters, status, viewsets
import rest_framework.permissions as permissions
from django.db.models import Exists, OuterRef


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    pagination_class = None
    search_fields = ('name')


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):

    serializer_class = RecipeListSerializer
    permission_classes= (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeListSerializer
        else:
            return RecipeCreationSerializer

    def get_queryset(self):
        user = self.request.user.id
        favorite = Favourite.objects.filter(
            user=user,
            recipe=OuterRef('pk')
        )
        shooping_cart = ShoppingCart.objects.filter(
            user=user,
            recipe=OuterRef('pk')
        )
        queryset = Recipe.objects.all().annotate(
            is_favorited=Exists(favorite),
            is_in_shopping_cart=Exists(shooping_cart)
        )
        return queryset

    