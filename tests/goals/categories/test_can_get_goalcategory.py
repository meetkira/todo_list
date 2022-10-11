import pytest

from goals.serializers import GoalCategorySerializer

@pytest.mark.django_db
def test_can_get_goalcategory(client, board_participant, goal_category, get_user_cookies):

    response = client.get(
        f"/goals/goal_category/{goal_category.id}",
        cookies=get_user_cookies
    )
    assert response.status_code == 200
    assert response.data == GoalCategorySerializer(goal_category).data
