from database import engine

from fastapi import FastAPI
import models

from routers import auth, todos

app = FastAPI()


# This automaticly searh for database.py and models.py
# and then create database.
models.Base.metadata.create_all(bind=engine)

app.include_router(auth.auth_router)
app.include_router(todos.todos_router)
