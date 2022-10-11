import pytest


@pytest.mark.django_db
def test_can_create_goalcomment(client, board_participant, goal, get_user_cookies):

    data = {
        "text": "test_comment",
        "goal": goal.id,
    }

    response = client.post(
        "/goals/goal_comment/create",
        data,
        content_type='application/json',
        cookies=get_user_cookies
    )

    assert response.status_code == 201
    assert response.data["text"] == "test_comment"
    assert response.data["goal"] == goal.id
