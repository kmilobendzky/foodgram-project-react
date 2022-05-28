from django.contrib.auth import get_user_model
from django.db import transaction
from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from users.models import Follow

from api.models import (Favourite, Ingredient, IngredientAmount, Recipe,
                        ShoppingCart, Tag)

User = get_user_model()


def is_subscribed(self, obj):
    user = self.context.get('request').user
    following = obj.id
    subscription = (Follow.objects.filter(
        user=user, following=following).exists() and user.is_authenticated)
    return subscription


class UserSerializer(UserSerializer):

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',)

    def get_is_subscribed(self, obj):
        return is_subscribed(self, obj)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
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
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class IngredientsTupleSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(min_value=1)
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = IngredientAmount
        fields = (
            'id',
            'amount',)


class RecipeListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(
        source='amount_recipe',
        many=True
    )
    is_favorited = serializers.BooleanField(read_only=True, required=False)
    is_in_shopping_cart = serializers.BooleanField(
        read_only=True, required=False)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart'
        )


class RecipeTupleSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',)
        read_only_fields = (
            'id',
            'name',
            'image',
            'cooking_time',)


class RecipeCreationSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    text = serializers.CharField()
    author = UserSerializer(required=False)
    ingredients = IngredientsTupleSerializer(
        many=True
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
    )
    cooking_time = serializers.IntegerField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
        )

    def validate(self, data):
        ingredients = data.get('ingredients')
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

    @staticmethod
    def add_tags_ingredients_to_recipe(tags, ingredients, recipe):
        for tag in tags:
            recipe.tags.add(tag)
        for ingredient in ingredients:
            IngredientAmount.objects.create(
                recipe=recipe, ingredient=ingredient['id'],
                amount=ingredient['amount']
            )

    @transaction.atomic
    def create(self, validated_data):
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)
        self.add_tags_ingredients_to_recipe(
            tags,
            ingredients,
            recipe)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.tags.clear()
        IngredientAmount.objects.filter(recipe=instance).delete()
        self.add_tags_ingredients_to_recipe(
            validated_data.pop('tags'),
            validated_data.pop('ingredients'),
            instance)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeListSerializer(instance, context=self.context).data


class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = (
            'user',
            'recipe',
        )

    def validate(self, data):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        recipe = data['recipe']
        if Favourite.objects.filter(
            user=request.user,
                recipe=recipe).exists():
            raise serializers.ValidationError({
                'status': 'Рецепт уже есть в избранном!'
            })
        return data

    def to_representation(self, instance):
        return RecipeTupleSerializer(
            instance,
            context=self.context).data


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = (
            'user',
            'recipe',
        )

    def to_representation(self, instance):
        return RecipeTupleSerializer(
            instance,
            context=self.context).data
