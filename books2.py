from typing import Optional

from fastapi import FastAPI, Path
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: float
    publish_date: int

    def __init__(
        self,
        id: int,
        title: str,
        author: str,
        description: str,
        rating: float,
        publish_date: int,
    ) -> None:
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.publish_date = publish_date


class Book_request(BaseModel):
    id: Optional[int] = Field(
        description="Id is not needed on create", default=None
    )
    title: str = Field(min_length=3, max_length=100)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: float = Field(gt=0, lt=6)
    publish_date: int = Field(gt=2000, lt=2026)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new Book",
                "author": "burhanudin",
                "description": "Nice book for legend",
                "rating": 5,
                "publish_date": 2021,
            }
        }
    }


# --------------------------------------------------------------
#
#
#
# --------------------------------------------------------------

BOOKS = [
    Book(1, "Computer science Pro", "ruby", "nice book", 5, 2021),
    Book(2, "Be Fast with FastAPI", "cow", "Great book", 5, 2021),
    Book(3, "Master", "ruby", "A book", 5, 2021),
    Book(4, "HP1", "Author 1", "Books description", 2, 2021),
    Book(5, "HP2", "Author 2", "Books description", 3, 2024),
    Book(6, "HP3", "Author 3", "Books description", 1, 2024),
]


@app.get("/books")
def read_all_books():
    return BOOKS


@app.get("/books/{book_id}")
def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book


@app.get("/books/")
def read_book_by_rating(book_rating: int):
    books_to_return: list[Book] = []

    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)

    return books_to_return


@app.post("/create-book")
def create_book(book_request: Book_request):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


@app.put("/books/update-book")
def update_book(book: Book_request):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book  # type: ignore


@app.delete("/books/{book_id}")
def delete_book(book_id: int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break


@app.get("/books/publish/")
def get_book_by_publish_date(publish_date: int):
    books_to_return: list[Book] = []
    for book in BOOKS:
        if book.publish_date == publish_date:
            books_to_return.append(book)

    return books_to_return


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1  # ternary
    return book
