import pytest

try:
    from backend.api.models import Tag
except ImportError:
    assert False, 'Не найдена модель Tag'


try:
    from backend.api.models import Ingredient
except ImportError:
    assert False, 'Не найдена модель Ingredient'

try:
    from backend.api.models import Recipe
except ImportError:
    assert False, 'Не найдена модель Recipe'