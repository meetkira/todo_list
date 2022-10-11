import pytest

from goals.models import GoalCategory


@pytest.mark.django_db
def test_can_drop_goalcategory(client, board_participant, goal_category, get_user_cookies):

    response = client.delete(
        f"/goals/goal_category/{goal_category.id}",
        cookies=get_user_cookies,
    )
    assert response.status_code == 204
    goal_category_ = GoalCategory.objects.get(id=goal_category.id)
    assert goal_category_.is_deleted
