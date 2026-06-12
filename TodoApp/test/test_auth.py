from .utils import *
from ..routers.auth import get_db, authenticate_user

app.dependency_overrides[get_db] = override_get_db


def test_auth_user(test_user):  # type: ignore
    db = TestingSessionLocal()

    authenticated_user = authenticate_user(
        test_user.username, "bani", db  # type: ignore
    )

    if authenticated_user:
        assert authenticated_user is not None
        assert authenticated_user.username == test_user.username  # type: ignore

    non_auth_user = authenticate_user("WrongUsername", "bani", db)
    assert non_auth_user is False

    wrong_password = authenticate_user(test_user.username, "bani123", db)  # type: ignore
    assert wrong_password is False
