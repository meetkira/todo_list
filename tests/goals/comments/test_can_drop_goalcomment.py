import pytest

from goals.models import GoalComment


@pytest.mark.django_db
def test_can_drop_goalcomment(client, board_participant, goal_comment, get_user_cookies):

    response = client.delete(
        f"/goals/goal_comment/{goal_comment.id}",
        cookies=get_user_cookies,
    )
    assert response.status_code == 204
    goal_comment_ = GoalComment.objects.filter(id=goal_comment.id).first()
    assert goal_comment_ is None
