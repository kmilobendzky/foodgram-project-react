import tempfile

import pytest


@pytest.fixture
def tag():
    from backend.api.models import Tag
    return Tag.objects.create(name='first_tag', color='Синий', slug='ftag')

@pytest.fixture
def tag_2():
    from backend.api.models import Tag
    return Tag.objects.create(name='second_tag', color='Красный', slug='stag')

@pytest.fixture
def ingredient():
    from backend.api.models import Ingredient
    return Ingredient.objects.create(name='Говядина', measurement_unit='г')

@pytest.fixture
def ingredient_2():
    from backend.api.models import Ingredient
    return Ingredient.objects.create(name='Свинина', measurement_unit='г')