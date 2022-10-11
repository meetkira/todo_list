import pytest


@pytest.fixture
@pytest.mark.django_db
def create_user_cookies(client, django_user_model):
    username = "testuser"
    password = "testuserpassword"

    django_user_model.objects.create_user(username=username, password=password)

    response = client.post(
        "/core/login",
        {"username": username, "password": password},
        content_type='application/json',
    )

    return response.cookies


@pytest.fixture
@pytest.mark.django_db
def get_user_cookies(client):
    username = "testuser"
    password = "testuserpassword"

    response = client.post(
        "/core/login",
        {"username": username, "password": password},
        content_type='application/json',
    )

    return response.cookies
