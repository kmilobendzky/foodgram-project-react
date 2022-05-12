import pytest
from django.contrib.auth import get_user_model

from backend.api.models import Tag


class TestTagAPI:

    @pytest.mark.django_db(transaction=True)
    def test_tags_not_found(self, user_client):
        response = user_client.get('/api/tags/')

        assert response.status_code != 404, (
            'Страница `/api/tags/` не найдена, проверьте этот адрес в *urls.py*'
        )

    @pytest.mark.django_db(transaction=True)
    def test_tag_id_not_found(self, user_client, tag):
        response = user_client.get(f'/api/tags/{tag.id}/')
        assert response.status_code != 404, (
            f'Тег с tag_id {tag.id} не найден, проверьте правильность работы urls.py и view-функции'
        )

class TestIngredientAPI:
    @pytest.mark.django_db(transaction=True)
    def test_ingredients_not_found(self, user_client):
        response = user_client.get('/api/ingredients/')

        assert response.status_code != 404, (
            'Страница `/api/ingredients/` не найдена, проверьте этот адрес в *urls.py*'
        )