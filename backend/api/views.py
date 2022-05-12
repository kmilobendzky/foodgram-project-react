import rest_framework.permissions as permissions
from api.models import (Favourite, Ingredient, IngredientAmount, Recipe,
                        ShoppingCart, Tag)
from api.serializers import (FavouriteSerializer, IngredientSerializer,
                             RecipeCreationSerializer, RecipeListSerializer,
                             ShoppingCartSerializer, TagSerializer)
from api.pagination import CustomPaginationClass
from django.db.models import Exists, OuterRef, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


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

    def deletion_method(request, pk, model):
        user = request.user.id
        recipe = get_object_or_404(Recipe, id=pk)
        obj = get_object_or_404(model, user=user, recipe=recipe)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['POST'],
        url_path='favorite',
        permission_classes=[permissions.IsAuthenticated]
        )
    def create_favorite(self, request, pk):
        return self.creation_method(
            request=request,
            pk=pk,
            serializers=FavouriteSerializer)

    @action(
        detail=True,
        methods=['DELETE'],
        url_path='favorite',
        permission_classes=[permissions.IsAuthenticated]
        )
    def delete_favorite(self, request, pk):
        return self.deletion_method(
            request=request,
            pk=pk,
            serializers=FavouriteSerializer)
    
    @action(
        detail=True,
        methods=['POST'],
        url_path='shopping_cart',
        permission_classes=[permissions.IsAuthenticated]
        )
    def create_shopping_cart(self, request, pk):
        return self.creation_method(
            request=request,
            pk=pk,
            serializers=ShoppingCartSerializer)

    @action(
        detail=True,
        methods=['DELETE'],
        url_path='shopping_cart',
        permission_classes=[permissions.IsAuthenticated]
        )
    def delete_favorite(self, request, pk):
        return self.deletion_method(
            request=request,
            pk=pk,
            serializers=ShoppingCartSerializer)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[permissions.IsAuthenticated]
        )
    def download_shopping_cart(self, request):
        shopping_list = {}
        ingredients = IngredientAmount.objects.filter(
            recipe__recipe_carts__user=request.user).values_list(
                'ingredient__name',
                'inredient_measurements_unit',
            ).annotate(amount=Sum('amount'))
        for ingredient in ingredients:
            ingredient_name = ingredient[0]
            if ingredient_name not in shopping_list:
                shopping_list[ingredient_name] = {
                    'measurement_unit': ingredient[1],
                    'amount': ingredient[2],
                }
            else:
                shopping_list[ingredient_name]['amount'] += ingredient[2]

        pdfmetrics.registerFont(
            TTFont('Handicraft', 'data/Handicraft.ttf', 'UTF-8')
        )
        response = HttpResponse(
            content_type='application/pdf')
        response['Content-Disposition'] = (
            'attachment; filename="shopping_list.txt"'
            )
        page = canvas.Canvas(response)
        page.setFont('Handicraft', size=20)
        page.drawString(200, 800, 'Список покупок')
        page.setFont('Handicraft', size=16)
        height = 800
        for ing, (name, data) in enumerate(
            shopping_list.items(), 1):
            page.drawString(
                75, height, (
                    f'{ing}. {name} - {data["amount"]} '
                    f'{data["measurement_unit"]}')
                    )
            height -= 25
        page.showPage()
        page.save()
        return response