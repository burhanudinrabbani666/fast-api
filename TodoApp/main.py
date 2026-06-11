from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, status, Path
from database import engine, Sessionlocal
from sqlalchemy.orm import Session

import models
from models import Todos

app = FastAPI()


# This automaticly searh for database.py and models.py
# and then create database.
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


db_depedency = Annotated[Session, Depends(get_db)]


@app.get("/", status_code=status.HTTP_200_OK, tags=["Books"])
async def read_all(db: db_depedency):
    return db.query(Todos).all()


@app.get(
    "/todos/{todo_id}",
    status_code=status.HTTP_200_OK,
    tags=["Books"],
)
async def read_todo(db: db_depedency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is not None:
        return todo_model

    raise HTTPException(status_code=404, detail="Todo not found")
