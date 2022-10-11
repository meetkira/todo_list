import pytest

from goals.serializers import GoalSerializer

@pytest.mark.django_db
def test_can_get_goal(client, board_participant, goal, get_user_cookies):

    response = client.get(
        f"/goals/goal/{goal.id}",
        cookies=get_user_cookies
    )
    assert response.status_code == 200
    assert response.data == GoalSerializer(goal).data
