from typing import Annotated, Any
from pydantic import BaseModel
from database import Sessionlocal

from passlib.context import CryptContext
from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from .auth import get_current_user
from models import Users

router = APIRouter(prefix="/users", tags=["Users"])

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class NewPasswordRequest(BaseModel):
    password: str
    new_password: str


"""
---------------------------------------------------------------------
FUNCTION
---------------------------------------------------------------------

"""


def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


db_depedency = Annotated[Session, Depends(get_db)]

user_depedency = Annotated[
    dict[str, Any] | None, Depends(get_current_user)
]


def get_user_from_database(id: Any, db: db_depedency) -> Users | None:
    return db.query(Users).filter(Users.id == id).first()


"""
---------------------------------------------------------------------
ROUTE
---------------------------------------------------------------------

"""


@router.get("/get_user")
async def get_user(user: user_depedency, db: db_depedency):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication Failed",
        )

    current_user = get_user_from_database(user.get("id"), db)

    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return current_user


@router.post(
    "/change_user",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def change_user(
    user: user_depedency,
    db: db_depedency,
    new_password_request: NewPasswordRequest = Body(),
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication Failed",
        )

    current_user = get_user_from_database(user.get("id"), db)
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Verify old password
    if not bcrypt_context.verify(
        new_password_request.password, current_user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication Failed",
        )

    current_user.hashed_password = bcrypt_context.hash(
        new_password_request.new_password
    )

    db.add(current_user)
    db.commit()
