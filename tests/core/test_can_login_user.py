import pytest


@pytest.mark.django_db
def test_can_login_user(client, django_user_model):
    username = "testuser"
    password = "testuserpassword"

    django_user_model.objects.create_user(username=username, password=password)

    response = client.post(
        "/core/login",
        {"username": username, "password": password},
        content_type='application/json',
    )

    assert response.status_code == 200
    assert response.data == {'username': 'testuser', 'first_name': '', 'last_name': '', 'email': ''}
    assert response.cookies is not None
