import pytest


@pytest.mark.django_db
def test_can_create_goalcategory(client, board_participant, get_user_cookies):

    data = {
        "title": "test_category",
        "board": board_participant.board.id
    }

    response = client.post(
        "/goals/goal_category/create",
        data,
        content_type='application/json',
        cookies=get_user_cookies
    )

    assert response.status_code == 201
    assert response.data["board"] == board_participant.board.id
    assert response.data["title"] == "test_category"
