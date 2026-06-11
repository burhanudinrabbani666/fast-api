from typing import Annotated
from pydantic import BaseModel, Field
from database import Sessionlocal

from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session

from models import Todos

todos_router = APIRouter()


def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


db_depedency = Annotated[Session, Depends(get_db)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


@todos_router.get(
    "/todos",
    status_code=status.HTTP_200_OK,
    tags=["Todos"],
)
async def read_all(db: db_depedency):
    return db.query(Todos).all()


@todos_router.get(
    "/todos/{todo_id}",
    status_code=status.HTTP_200_OK,
    tags=["Todos"],
)
async def read_todo(db: db_depedency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is not None:
        return todo_model

    raise HTTPException(status_code=404, detail="Todo not found")


@todos_router.post(
    "/todos",
    status_code=status.HTTP_201_CREATED,
    tags=["Todos"],
)
async def create_todo(db: db_depedency, todo_request: TodoRequest):
    todo_model = Todos(**todo_request.model_dump())

    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)

    return todo_model


@todos_router.put(
    "/todos/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Todos"],
)
async def update_todo(
    db: db_depedency,
    todo_request: TodoRequest,
    todo_id: int = Path(gt=0),
):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(
            status_code=204,
            detail="Todo not found",
        )

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()


@todos_router.delete(
    "/todos/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Todos"],
)
async def delete_todo(db: db_depedency, todo_id: int = Path(gt=0)):
    result = db.query(Todos).filter(Todos.id == todo_id).delete()
    if result == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )

    db.commit()
