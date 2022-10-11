import pytest

from core.serializers import ProfileSerializer


@pytest.mark.django_db
def test_can_get_profile(client, user, get_user_cookies):

    response = client.get(
        f"/core/profile",
        cookies=get_user_cookies
    )
    assert response.status_code == 200
    assert response.data == ProfileSerializer(user).data
