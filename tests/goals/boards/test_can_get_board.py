import pytest

from goals.serializers import BoardSerializer


@pytest.mark.django_db
def test_can_get_board(client, board_participant, board, get_user_cookies):

    response = client.get(
        f"/goals/board/{board.id}",
        cookies=get_user_cookies
    )
    assert response.status_code == 200
    assert response.data == BoardSerializer(board).data
