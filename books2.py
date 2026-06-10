from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

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


class Book_request(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3, max_length=100)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: float = Field(gt=1, lt=6)


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


@app.post("/create-book")
def create_book(book_request: Book_request):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1  # ternary
    return book
