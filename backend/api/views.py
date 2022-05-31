import rest_framework.permissions as permissions
from django.db.models import Exists, OuterRef, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import (Favourite, Ingredient, IngredientAmount, Recipe,
                        ShoppingCart, Tag)
from api.pagination import CustomPaginationClass
from api.serializers import (FavouriteSerializer, IngredientSerializer,
                             RecipeCreationSerializer, RecipeListSerializer,
                             ShoppingCartSerializer, TagSerializer)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    pagination_class = CustomPaginationClass
    search_fields = 'name'


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = CustomPaginationClass


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = CustomPaginationClass

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeListSerializer
        return RecipeCreationSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        favorite = Favourite.objects.filter(
            user=user_id,
            recipe=OuterRef('pk')).all()
        shooping_cart = ShoppingCart.objects.filter(
            user=user_id,
            recipe=OuterRef('pk')).all()
        queryset = Recipe.objects.all().annotate(
            is_favorited=Exists(favorite),
            is_in_shopping_cart=Exists(shooping_cart))
        return queryset

    @staticmethod
    def creation_method(request, pk, serializers):
        user = request.user.id
        data = {
            'user': user,
            'recipe': pk,
        }
        serializer = serializers(
            data=data,
            context={
                'request': request
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def deletion_method(request, pk, model):
        user = request.user.id
        recipe = get_object_or_404(Recipe, id=pk)
        obj = get_object_or_404(model, user=user, recipe=recipe)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        url_path='favorite',
        permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk):
        if self.request.method == 'POST':
            return self.creation_method(
                request=request,
                pk=pk,
                serializers=FavouriteSerializer)
        elif self.request.method == 'DELETE':
            return self.deletion_method(
                request=request,
                pk=pk,
                model=Favourite)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        url_path='shopping_cart',
        permission_classes=[permissions.IsAuthenticated])
    def shopping_cart(self, request, pk):
        if self.request.method == 'POST':
            return self.creation_method(
                request=request,
                pk=pk,
                serializers=ShoppingCartSerializer)
        elif self.request.method == 'DELETE':
            return self.deletion_method(
                request=request,
                pk=pk,
                model=ShoppingCart)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        file_name = 'shopping_list.txt'
        forming_list = {}
        final_list = []
        ingredients = IngredientAmount.objects.filter(
            recipe__cart_recipe__user=request.user).values_list(
                'ingredient__name',
                'ingredient__measurement_unit',).annotate(amount=Sum('amount'))
        for ingredient in ingredients:
            ingredient_name = ingredient[0]
            if ingredient_name not in forming_list:
                forming_list[ingredient_name] = {
                    'measurement_unit': ingredient[1],
                    'amount': ingredient[2],
                }
            else:
                forming_list[ingredient_name]['amount'] += ingredient[2]
            final_list = ['Ingredient list\n\n']
        for ingredient, value in forming_list.items():
            final_list.append(
                f' {ingredient} - {value["amount"]} '
                f'{value["measurement_unit"]}\n')
        return HttpResponse(
            final_list,
            {
                'Content-Type': 'text/plain',
                'Content-Disposition':
                f'attachment; filename={file_name}',
            },
        )
