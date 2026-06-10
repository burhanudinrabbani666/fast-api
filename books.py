from fastapi import FastAPI, Body

app = FastAPI()


BOOKS: list[dict[str, str]] = [
    {
        "title": "Title One",
        "author": "author One",
        "category": "science",
    },
    {
        "title": "Title Two",
        "author": "author Two",
        "category": "science",
    },
    {
        "title": "Title Three",
        "author": "author Three",
        "category": "history",
    },
    {
        "title": "Title Four",
        "author": "author Four",
        "category": "math",
    },
    {
        "title": "Title Five",
        "author": "author Five",
        "category": "math",
    },
    {
        "title": "Title Six",
        "author": "author Two",
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


@app.get("/books/", tags=["Books"])
async def get_book_by_query(category: str):
    books_to_return: list[dict[str, str]] = []
    for book in BOOKS:
        if book.get("category", "").casefold() == category.casefold():
            books_to_return.append(book)

    return books_to_return


@app.get("/books/{book_author}/", tags=["Books"])
async def get_author_category_by_query(
    book_author: str, category: str
):
    books_to_return: list[dict[str, str]] = []

    for book in BOOKS:
        if (
            book.get("author", "").casefold()
            == book_author.casefold()
            and book.get("category", "").casefold()
            == category.casefold()
        ):
            books_to_return.append(book)

    return books_to_return


@app.post("/books", tags=["Books"])
async def create_new_book(
    new_book: dict[str, str] = Body(),
):
    BOOKS.append(new_book)
    return new_book


@app.put("/books/update_book", tags=["Books"])
async def update_book(updated_book: dict[str, str] = Body()):
    for i in range(len(BOOKS)):
        if (
            BOOKS[i].get("title", "").casefold()
            == updated_book.get("title", "").casefold()
        ):
            BOOKS[i] = updated_book


@app.delete("/books/{book_title}", tags=["Books"])
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if (
            BOOKS[i].get("title", "").casefold()
            == book_title.casefold()
        ):
            BOOKS.pop(i)
