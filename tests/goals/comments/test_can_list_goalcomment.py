import pytest

from goals.serializers import GoalCommentSerializer
from tests.factories import GoalCommentFactory


@pytest.mark.django_db
def test_can_list_goal(client, board_participant, goal, get_user_cookies):
    comments = GoalCommentFactory.create_batch(3, user=board_participant.user, goal=goal)

    expected_result = {
        "count": 3,
        "next": None,
        "previous": None,
        "results": GoalCommentSerializer(comments, many=True).data
    }

    response = client.get(
        "/goals/goal_comment/list",
        data={"goal": goal.id},
        cookies=get_user_cookies
    )
    assert response.status_code == 200
    assert response.data == expected_result
