from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()

class Tag(models.Model):
    BLUE = '#06266F'
    RED = '#A60000'
    YELLOW = '#FFBE00'
    GREEN = '#008500'
    ORANGE = '#FF7400'
    PURPLE = '#CD0074'
    TURQUOISE = '#028E9B'

    COLOR_CHOICES = [
        (BLUE, 'Синий'),
        (RED, 'Красный'),
        (YELLOW, 'Желтый'),
        (GREEN, 'Зеленый'),
        (ORANGE, 'Оранжевый'),
        (PURPLE, 'Пурпурный'),
        (TURQUOISE, 'Бирюзовый'),
    ]

    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Название тега',
    )
    color = models.CharField(
        max_length=7,
        choices=COLOR_CHOICES,
        unique = True,
        verbose_name='Цвет',
    )
    slug = models.SlugField(
        max_length=150,
        unique=True,
        verbose_name='Slug',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'{self.name}'

class Ingredient(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name='Название',
    )
    measurment_unit = models.CharField(
        max_length=150,
        verbose_name='Единица измерения',
    )

    class Meta:
        ordering = ['id',]
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}'

class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        related_name='recipe_tags',
        verbose_name='Тег',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe_author',
        verbose_name='Автор',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipe_ingredients',
        verbose_name='Ингредиент',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название',)
    image = models.ImageField(
        upload_to='media/',
        verbose_name='Изображение',)
    text = models.TextField(
        max_length=4000,
        verbose_name='Описание',)
    coocking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=[MinValueValidator(
            1,
            message='Минимальное время приготовления - 1 минута!'),],
    )


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='amount_ingredient',
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='amount_recipe',
        verbose_name='Рецепт',
    )
    count = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[MinValueValidator],
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'

    def __str__(self):
        return f'{self.ingredient}: {self.recipe}'


class Favourite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favourite_recipe',
        verbose_name='Избранный рецепт',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'

    def __str__(self):
        return f'{self.user}: {self.recipe}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart_user',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart_recipe',
        verbose_name='Рецепт',
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return f'{self.user}: {self.recipe}'
