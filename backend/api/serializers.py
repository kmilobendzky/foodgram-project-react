from api.models import (Favourite, Ingredient, IngredientAmount, Recipe,
                        ShoppingCart, Tag)
from drf_extra_fields.fields import Base64ImageField
from users.models import Follow
from rest_framework import serializers
from users.serializers import UserSerializer
from django.contrib.auth import get_user_model


User = get_user_model()

class TagSerializer(serializers.ModelSerializer):
    model = Tag
    fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    model = Ingredient
    fields = '__all__'

class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )
    class Meta:
        model = IngredientAmount
        fields = {
            'id',
            'name',
            'measurement_unit',
            'amount',
        }

class IngredientsTupleSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )
    amount = serializers.IntegerField(min_value=1)

    class Meta:
        model = IngredientAmount
        fields = (
            'id',
            'amount',
            )


class RecipeTupleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = {
            'id',
            'name',
            'image',
            'cooking_time',
        }


class RecipeListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    class Meta:
        model = Recipe
        fields = {
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'coocking_time',
            'is_favorited',
            'is_in_shopping_cart',
        }

    def get_ingredients(self, obj):
        ingredients_list = IngredientAmount.objects.filter(recipe=obj)
        ingredients_data = IngredientAmountSerializer(ingredients_list, many=True).data
        return ingredients_data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        user = request.user
        if not request or not user.is_authenticated:
            return False
        favorite_exists = Favourite.objects.filter(recipe=obj, user=user).exists()
        return favorite_exists

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        user = request.user
        if not request or not user.is_authenticated:
            return False
        shopping_cart_exists = ShoppingCart.objects.filter(
            recipe=obj,
            user=user
        )
        return shopping_cart_exists


class RecipeTupleSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    
    class Meta:
        model = Recipe
        fields = (
            'id', 
            'name', 
            'image', 
            'cooking_time')
        read_only_fields = (
            'id', 
            'name', 
            'image', 
            'cooking_time')
    
class RecipeCreationSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    text = serializers.CharField()
    author = UserSerializer()
    ingredients = IngredientsTupleSerializer(
        many=True
    )
    tags = serializers.PrimaryKeyReatedField(
        many=True,
        queryset=Tag.objects.all(),
    )
    cooking_time = serializers.IntegerField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = {
            'id',
            'author',
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
        }

    def add_stuff_to_recipe(recipe, tags, ingredients):
        for tag in tags:
            recipe.tags.add(tag)
        for ingredient in ingredients:
            IngredientAmount.objects.create(
                recipe=recipe, 
                amount=ingredient['amount'],
                ingredient=ingredient['id'],
            )

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError(
                'В рецепте должны быть ингредиенты!'
            )

        cooking_time = self.initial_data.get('cooking_time')
        if cooking_time < 1:
            raise serializers.ValidationError(
                'Время приготовления не может быть меньше 1!'
            )
        return data

    def create(self, validated_data):
        tags = validated_data.get('tags')
        ingredients = validated_data.get('ingredients')
        author=self.context.get('request').user
        recipe=Recipe.objects.create(
            author=author,
            **validated_data,
        )
        self.add_stuff_to_recipe(recipe, tags, ingredients)

    def update(self, recipe, validated_data):
        recipe.tags.clear()
        recipe.tags = validated_data.get('tags', recipe.image)
        recipe.image = validated_data.get('image', recipe.image)
        IngredientAmount.objects.filter(recipe=recipe).delete()
        recipe.name = validated_data.get('name', recipe.image)
        recipe.text = ('text', recipe.text)
        self.add_stuff_to_recipe(recipe, recipe.tags, recipe.ingredients)
        return recipe