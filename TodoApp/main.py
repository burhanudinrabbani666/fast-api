from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from .database import engine
from .models import Base
from .routers import auth, todos, admin, users

app = FastAPI()


# This automaticly searh for database.py and models.py
# and then create database.
Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="TodoApp/templates")

app.mount(
    "/static",
    StaticFiles(directory="TodoApp/static"),
    name="static",
)


@app.get("/")
def test(request: Request) -> Response:
    return templates.TemplateResponse(
        request=request, name="home.html"
    )


@app.get("/healthy")
async def health_check():
    return {"status": "Healthy"}


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
