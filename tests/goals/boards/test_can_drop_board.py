import pytest

from goals.models import Board


@pytest.mark.django_db
def test_can_drop_board(client, board_participant, board, get_user_cookies):
    response = client.delete(
        f"/goals/board/{board.id}",
        cookies=get_user_cookies,
    )
    assert response.status_code == 204
    board_ = Board.objects.get(id=board.id)
    assert board_.is_deleted
