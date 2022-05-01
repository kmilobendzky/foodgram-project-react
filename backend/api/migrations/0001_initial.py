# Generated by Django 3.2 on 2022-04-27 17:17

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название')),
                ('measurment_unit', models.CharField(max_length=150, verbose_name='Единица измерения')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('image', models.ImageField(upload_to='media/', verbose_name='Изображение')),
                ('text', models.TextField(max_length=4000, verbose_name='Описание')),
                ('coocking_time', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Минимальное время приготовления - 1 минута!')], verbose_name='Время приготовления')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_author', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('ingredients', models.ManyToManyField(related_name='recipe_ingredients', to='api.Ingredient', verbose_name='Ингредиент')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Название тега')),
                ('color', models.CharField(choices=[('#06266F', 'Синий'), ('#A60000', 'Красный'), ('#FFBE00', 'Желтый'), ('#008500', 'Зеленый'), ('#FF7400', 'Оранжевый'), ('#CD0074', 'Пурпурный'), ('#028E9B', 'Бирюзовый')], max_length=7, unique=True, verbose_name='Цвет')),
                ('slug', models.SlugField(max_length=150, unique=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_recipe', to='api.recipe', verbose_name='Рецепт')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_user', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Список покупок',
                'verbose_name_plural': 'Списки покупок',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_name='recipe_tags', to='api.Tag', verbose_name='Тег'),
        ),
        migrations.CreateModel(
            name='IngredientAmount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator], verbose_name='Количество')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='amount_ingredient', to='api.ingredient', verbose_name='Ингредиент')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='amount_recipe', to='api.recipe', verbose_name='Рецепт')),
            ],
            options={
                'verbose_name': 'Количество ингредиента',
                'verbose_name_plural': 'Количество ингредиентов',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Favourite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourite_recipe', to='api.recipe', verbose_name='Избранный рецепт')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранные',
                'ordering': ['-id'],
            },
        ),
    ]