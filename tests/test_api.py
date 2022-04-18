import pytest
from backend.api.models import Tag
from django.contrib.auth import get_user_model


class TestTagAPI:

    @pytest.mark.django_db(transaction=True)
    def test_tags_not_found(self, user_client):
        response = user_client.get(f'/api/tags/')

        assert response.status_code != 404, (
            'Страница `/api/tags/` не найдена, проверьте этот адрес в *urls.py*'
        )


    
    