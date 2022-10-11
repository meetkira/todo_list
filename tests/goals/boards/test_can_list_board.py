import pytest

from goals.serializers import BoardListSerializer
from tests.factories import BoardFactory, BoardParticipantFactory


@pytest.mark.django_db
def test_can_list_board(client, board_participant, get_user_cookies):
    boards = BoardFactory.create_batch(3)
    for board in boards:
        BoardParticipantFactory.create(user=board_participant.user, board=board)
    boards.append(board_participant.board)
    boards.sort(key=lambda x: x.title)

    expected_result = {
        "count": 4,
        "next": None,
        "previous": None,
        "results": BoardListSerializer(boards, many=True).data
    }

    response = client.get(
        "/goals/board/list",
        data={"limit": 10},
        cookies=get_user_cookies
    )
    assert response.status_code == 200
    assert response.data == expected_result
