import pytest

from goals.serializers import GoalCommentSerializer

@pytest.mark.django_db
def test_can_get_goalcomment(client, board_participant, goal_comment, get_user_cookies):

    response = client.get(
        f"/goals/goal_comment/{goal_comment.id}",
        cookies=get_user_cookies
    )
    assert response.status_code == 200
    assert response.data == GoalCommentSerializer(goal_comment).data
