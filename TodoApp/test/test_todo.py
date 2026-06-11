from typing import Any

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine, orm, text
import pytest


from ..database import Base
from ..main import app
from ..routers.todos import get_db
from ..routers.auth import get_current_user
from ..models import Todos

SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


TestingSessionLocal = orm.sessionmaker(autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_current_user() -> dict[str, Any]:
    return {"username": "bani123", "id": 1, "user_role": "admin"}


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_current_user

client = TestClient(app)


@pytest.fixture
def test_todo():
    todo = Todos(
        title="Learn Code",
        description="Need to learn everyday",
        priority=5,
        complete=True,
        owner_id=1,
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()

    yield todo
    with engine.connect() as connection:
        connection.execute(text("Delete from todos;"))
        connection.commit()


def test_read_all_authenticated(test_todo):
    response = client.get("/todos")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "title": "Learn Code",
            "complete": True,
            "description": "Need to learn everyday",
            "id": 1,
            "priority": 5,
            "owner_id": 1,
        }
    ]
