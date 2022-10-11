import pytest


@pytest.mark.django_db
def test_can_create_board(client, create_user_cookies):

    data = {
        "title": "test_board"
    }

    response = client.post(
        "/goals/board/create",
        data,
        content_type='application/json',
        cookies=create_user_cookies
    )

    assert response.status_code == 201
    assert response.data["id"] == 1
    assert response.data["title"] == 'test_board'
