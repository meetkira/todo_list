import pytest


@pytest.mark.django_db
def test_can_update_goal(client, board_participant, goal, get_user_cookies):
    data = {
        "category": goal.category.id,
        "description": None,
        "due_date": "2022-10-07",
        "priority": 2,
        "status": 1,
        "title": "test update title",
    }

    response = client.put(
        f"/goals/goal/{goal.id}",
        data=data,
        cookies=get_user_cookies,
        content_type='application/json',
    )
    assert response.status_code == 200
    assert response.data["title"] == "test update title"
    assert response.data["description"] is None
