from fastapi import FastAPI

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: float

    def __init__(
        self,
        id: int,
        title: str,
        author: str,
        description: str,
        rating: float,
    ) -> None:
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


BOOKS = [
    Book(
        1,
        "Computer science Pro",
        "codingwithruby",
        "A very nice book",
        5,
    ),
    Book(
        2,
        "Be Fast with FastAPI",
        "codingwithruby",
        "A very Great book",
        5,
    ),
    Book(
        3,
        "Master Chef",
        "codingwithruby",
        "A very Hell yah book",
        5,
    ),
    Book(
        4,
        "HP1",
        "Author 1",
        "Books description",
        2,
    ),
    Book(
        5,
        "HP2",
        "Author 2",
        "Books description",
        3,
    ),
    Book(
        6,
        "HP3",
        "Author 3",
        "Books description",
        1,
    ),
]


@app.get("/books")
def read_all_books():
    return BOOKS
