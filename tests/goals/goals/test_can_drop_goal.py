import pytest

from goals.models import Goal


@pytest.mark.django_db
def test_can_drop_goal(client, board_participant, goal, get_user_cookies):

    response = client.delete(
        f"/goals/goal/{goal.id}",
        cookies=get_user_cookies,
    )
    assert response.status_code == 204
    goal_ = Goal.objects.get(id=goal.id)
    assert goal_.is_deleted
