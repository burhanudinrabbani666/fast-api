from fastapi import FastAPI

app = FastAPI()

BOOKS: list[dict[str, str]] = [
    {
        "title": "Title One",
        "author": "authoe One",
        "category": "science",
    },
    {
        "title": "Title Two",
        "author": "authoe Two",
        "category": "science",
    },
    {
        "title": "Title Three",
        "author": "authoe Three",
        "category": "history",
    },
    {
        "title": "Title Four",
        "author": "authoe Four",
        "category": "math",
    },
    {
        "title": "Title Five",
        "author": "authoe Five",
        "category": "math",
    },
    {
        "title": "Title Six",
        "author": "authoe Two",
        "category": "math",
    },
]


@app.get("/books", tags=["Books"])
async def get_books():
    return BOOKS


@app.get("/books/{title}", tags=["Books"])
async def get_book_by_id(title: str):
    for book in BOOKS:
        if book.get("title", "").casefold() == title.casefold():
            return book
