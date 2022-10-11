import pytest


@pytest.mark.django_db
def test_can_update_goalcomment(client, board_participant, goal_comment, get_user_cookies):
    response = client.put(
        f"/goals/goal_comment/{goal_comment.id}",
        data={"text": "test update text"},
        cookies=get_user_cookies,
        content_type='application/json',
    )
    assert response.status_code == 200
    assert response.data["text"] == "test update text"
