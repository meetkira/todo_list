import pytest

@pytest.mark.django_db
def test_can_update_profile(client, user, get_user_cookies):

    data = {
        "username": user.username,
        "first_name": "test update first name",
        "last_name": "test update last name",
        "email": "testemail@mail.ru"
    }

    response = client.put(
        f"/core/profile",
        data=data,
        cookies=get_user_cookies,
        content_type='application/json',
    )
    assert response.status_code == 200
    assert response.data["first_name"] == "test update first name"
    assert response.data["last_name"] == "test update last name"
