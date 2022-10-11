import datetime

import pytest

from goals.models import Status


@pytest.mark.django_db
def test_can_create_goal(client, board_participant, goal_category, get_user_cookies):

    data = {
        "title": "test_goal",
        "description": "description of test goal",
        "category": goal_category.id,
        "due_date": datetime.date.today(),
    }

    response = client.post(
        "/goals/goal/create",
        data,
        content_type='application/json',
        cookies=get_user_cookies
    )

    assert response.status_code == 201
    assert response.data["title"] == "test_goal"
    assert response.data["description"] == "description of test goal"
    assert response.data["category"] == goal_category.id
    assert response.data["status"] == Status.to_do
