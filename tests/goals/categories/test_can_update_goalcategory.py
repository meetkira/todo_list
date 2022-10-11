import pytest

@pytest.mark.django_db
def test_can_update_goalcategory(client, board_participant, goal_category, get_user_cookies):

    response = client.put(
        f"/goals/goal_category/{goal_category.id}",
        data={"title": "test update title", "board": board_participant.board.id},
        cookies=get_user_cookies,
        content_type='application/json',
    )
    assert response.status_code == 200
    assert response.data["title"] == "test update title"
