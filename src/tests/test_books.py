import pytest
from fastapi import status
from sqlalchemy import select

from src.models.books import Book
from src.models.sellers import Seller


@pytest.mark.asyncio()
async def test_delete_book(db_session, async_client):
    seller = Seller(
        first_name="Olga",
        last_name="Buzova",
        email="best_singer@mail.com",
        password="malo_poloviN!",
    )
    db_session.add(seller)
    await db_session.flush()

    book = Book(
        title="Mtzyri",
        author="Lermontov",
        year=2023,
        pages=100,
        seller_id=seller.id,
    )
    db_session.add(book)
    await db_session.flush()

    response = await async_client.delete(f"/api/v1/books/{book.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    await db_session.flush()
    all_books = await db_session.execute(select(Book))
    res = all_books.scalars().all()
    assert len(res) == 0


@pytest.mark.asyncio()
async def test_delete_book_with_invalid_book_id(db_session, async_client):
    seller = Seller(
        first_name="Olga",
        last_name="Buzova",
        email="best_singer@mail.com",
        password="malo_poloviN!",
    )
    db_session.add(seller)
    await db_session.flush()

    book = Book(
        title="Mtzyri",
        author="Lermontov",
        year=2023,
        pages=100,
        seller_id=seller.id,
    )
    db_session.add(book)
    await db_session.flush()

    response = await async_client.delete(f"/api/v1/books/{book.id + 1}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio()
async def test_create_book(db_session, async_client):
    seller = Seller(
        first_name="Olga",
        last_name="Buzova",
        email="best_singer@mail.com",
        password="malo_poloviN!",
    )
    db_session.add(seller)
    await db_session.flush()

    book = {
        "title": "How to sing if bear stepped on your ear",
        "author": "Buzova Olga",
        "year": 2022,
        "count_pages": 7,
        "seller_id": seller.id,
    }

    response = await async_client.post("/api/v1/books/", json=book)
    assert response.status_code == status.HTTP_201_CREATED

    result_data = response.json()
    response_book_id = result_data.pop("id", None)
    assert response_book_id, "Book id not returned from endpoint"

    assert result_data == {
        "title": "How to sing if bear stepped on your ear",
        "author": "Buzova Olga",
        "year": 2022,
        "pages": 7,
        "seller_id": seller.id,
    }


@pytest.mark.asyncio()
async def test_create_book_with_invalid_year(db_session, async_client):
    seller = Seller(
        first_name="Olga",
        last_name="Buzova",
        email="best_singer@mail.com",
        password="malo_poloviN!",
    )
    db_session.add(seller)
    await db_session.flush()

    book = {
        "title": "'Dom 2' made a person of me",
        "author": "Buzova Olga",
        "year": 2000,
        "count_pages": 35,
        "seller_id": seller.id,
    }

    response = await async_client.post("/api/v1/books/", json=book)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_get_books(db_session, async_client):
    seller = Seller(
        first_name="Olga",
        last_name="Buzova",
        email="best_singer@mail.com",
        password="malo_poloviN!",
    )
    db_session.add(seller)
    await db_session.flush()

    book = Book(
        title="How to sing if bear stepped on your ear",
        author="Buzova Olga",
        year=2022,
        pages=7,
        seller_id=seller.id,
    )

    book2 = Book(
        title="Say yes for money",
        author="Zoteeva Dasha",
        year=2023,
        pages=100,
        seller_id=seller.id,
    )
    db_session.add_all([book, book2])
    await db_session.flush()

    response = await async_client.get("/api/v1/books/")
    assert response.status_code == status.HTTP_200_OK

    assert (len(response.json()["books"]) == 2)

    assert response.json() == {
        "books": [
            {
                "id": book.id,
                "title": "How to sing if bear stepped on your ear",
                "author": "Buzova Olga",
                "year": 2022,
                "pages": 7,
                "seller_id": seller.id,
            },
            {
                "id": book2.id,
                "title": "Say yes for money",
                "author": "Zoteeva Dasha",
                "year": 2023,
                "pages": 100,
                "seller_id": seller.id,
            },
        ],
    }


@pytest.mark.asyncio()
async def test_get_single_book(db_session, async_client):
    seller = Seller(
        first_name="Olga",
        last_name="Buzova",
        email="best_singer@mail.com",
        password="malo_poloviN!",
    )
    db_session.add(seller)
    await db_session.flush()

    book = Book(
        title="How to sing if bear stepped on your ear",
        author="Buzova Olga",
        year=2022,
        pages=7,
        seller_id=seller.id,
    )

    book2 = Book(
        title="Say yes for money",
        author="Zoteeva Dasha",
        year=2023,
        pages=100,
        seller_id=seller.id,
    )

    db_session.add_all([book, book2])
    await db_session.flush()

    response = await async_client.get(f"/api/v1/books/{book.id}")

    assert response.status_code == status.HTTP_200_OK

    assert response.json() == {
        "id": book.id,
        "title": "How to sing if bear stepped on your ear",
        "author": "Buzova Olga",
        "year": 2022,
        "pages": 7,
        "seller_id": seller.id,
    }


@pytest.mark.asyncio()
async def test_update_book(db_session, async_client):
    seller = Seller(
        first_name="Olga", last_name="Buzova",
        email="best_singer@mail.com", password="malo_poloviN!",
    )
    db_session.add(seller)
    await db_session.flush()

    book = Book(
        title="How to sing if bear stepped on your ear",
        author="Buzova Olga", year=2022,
        pages=7, seller_id=seller.id,
    )
    db_session.add(book)
    await db_session.flush()

    new_book_data = {
        "id": book.id, "title": "What to do if you enter the wrong door",
        "author": "Kirkorov Philippe", "year": 2023,
        "pages": 18335, "seller_id": seller.id,
    }

    response = await async_client.put(
        f"/api/v1/books/{book.id}", json=new_book_data,
    )
    assert response.status_code == status.HTTP_200_OK

    await db_session.flush()
    res = await db_session.get(Book, book.id)

    assert res.title == "What to do if you enter the wrong door"
    assert res.author == "Kirkorov Philippe"
    assert res.year == 2023
    assert res.pages == 18335
    assert res.id == book.id
    assert res.seller_id == seller.id
