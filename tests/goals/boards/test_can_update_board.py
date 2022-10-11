import pytest

@pytest.mark.django_db
def test_can_update_board(client, board_participant, board, get_user_cookies):

    response = client.put(
        f"/goals/board/{board.id}",
        data={"title": "test update title", "participants": []},
        cookies=get_user_cookies,
        content_type='application/json',
    )
    assert response.status_code == 200
    assert response.data["title"] == "test update title"
