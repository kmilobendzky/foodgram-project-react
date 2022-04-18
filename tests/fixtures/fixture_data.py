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

