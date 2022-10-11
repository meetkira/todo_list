import pytest

from goals.serializers import GoalCategorySerializer
from tests.factories import GoalCategoryFactory

@pytest.mark.django_db
def test_can_list_goalcategory(client, board_participant, get_user_cookies):

    categories = GoalCategoryFactory.create_batch(3, user=board_participant.user, board=board_participant.board)
    categories.sort(key=lambda x: x.title)

    expected_result = {
        "count": 3,
        "next": None,
        "previous": None,
        "results": GoalCategorySerializer(categories, many=True).data
    }

    response = client.get(
        "/goals/goal_category/list",
        data={"limit": 10},
        cookies=get_user_cookies
    )
    assert response.status_code == 200
    assert response.data == expected_result
