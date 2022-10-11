import pytest

from goals.serializers import GoalSerializer
from tests.factories import GoalFactory

@pytest.mark.django_db
def test_can_list_goal(client, board_participant, goal_category, get_user_cookies):

    goals = GoalFactory.create_batch(3, user=board_participant.user, category=goal_category)
    goals.sort(key=lambda x: x.title)

    expected_result = {
        "count": 3,
        "next": None,
        "previous": None,
        "results": GoalSerializer(goals, many=True).data
    }

    response = client.get(
        "/goals/goal/list",
        cookies=get_user_cookies
    )
    assert response.status_code == 200
    assert response.data == expected_result
