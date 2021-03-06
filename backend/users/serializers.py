from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from .models import Follow
from api.models import Recipe
from api.serializers import RecipeTupleSerializer

User = get_user_model()


class UserCreationSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'password',
            'first_name',
            'last_name',)
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'password': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True}, }


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
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        return Follow.objects.filter(user=user, following=obj).exists()


class FollowSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(
        source='user.email')
    id = serializers.ReadOnlyField(
        source='following.id'
    )
    username = serializers.ReadOnlyField(
        source='following.username'
    )
    first_name = serializers.ReadOnlyField(
        source='following.first_name'
    )
    last_name = serializers.ReadOnlyField(
        source='following.last_name'
    )
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        following = obj.id
        subscription = Follow.objects.filter(
            user=user, following=following).exists()
        return subscription

    def get_recipes(self, obj):
        author = obj.following
        tuple = Recipe.objects.filter(author=author)
        recipes = RecipeTupleSerializer(
            tuple,
            many=True)
        return recipes.data

    def get_recipes_count(self, obj):
        author = obj.id
        count = Recipe.objects.filter(author=author).count()
        return count
