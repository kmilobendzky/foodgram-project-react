from api.views import IngredientViewSet, RecipeViewSet, TagViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

api_routes = DefaultRouter()
api_routes.register('tags', TagViewSet, basename='tags',)
api_routes.register('ingredients', IngredientViewSet, basename='ingredients',)
api_routes.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path("", include(api_routes.urls)),
]