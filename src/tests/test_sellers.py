import pytest
from src.models.books import Book
from src.models.sellers import Seller
from fastapi import status
from sqlalchemy import select
from icecream import ic




@pytest.mark.asyncio
async def test_create_seller_with_weak_password(db_session, async_client):
    seller = {
        "first_name": "Olga",
        "last_name": "Buzova",
        "email": "best_singer@mail.com",
        "password": "arbuz"
    }

    response = await async_client.post("/api/v1/sellers/", json=seller)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

@pytest.mark.asyncio
async def test_create_seller(db_session, async_client):
    seller = {
        "first_name": "Olga",
        "last_name": "Buzova",
        "email": "best_singer@mail.com",
        "password": "malo_poloviN!"
    }

    response = await async_client.post("/api/v1/sellers/", json=seller)

    assert response.status_code == status.HTTP_201_CREATED

    result_data = response.json()

    response_seller_id = result_data.pop("id", None)
    assert response_seller_id, "Seller id not returned from endpoint"

    assert result_data == {
        "first_name": "Olga",
        "last_name": "Buzova",
        "email": "best_singer@mail.com",
        "password": "**********"
    }

@pytest.mark.asyncio
async def test_get_all_sellers(db_session, async_client):
    seller = Seller(
        first_name="Olga", last_name="Buzova",
        email="best_singer@mail.com", password="malo_poloviN!"
    )

    seller2 = Seller(
        first_name="Dasha", last_name="Zoteeva",
        email="instasamka@mail.com", password="Za_dengi_Da!"
    )
    db_session.add_all([seller, seller2])
    await db_session.flush()

    response = await async_client.get("/api/v1/sellers/")

    assert response.status_code == status.HTTP_200_OK

    assert len(response.json()["sellers"]) == 2

    assert response.json() == {
        "sellers": [
            {
                "first_name": "Olga", "last_name": "Buzova",
                "id": seller.id, "email": "best_singer@mail.com",
                "books": []
            },
            {
                "first_name": "Dasha", "last_name": "Zoteeva",
                "id": seller2.id, "email": "instasamka@mail.com",
                "books": []
            }
        ]
    }

@pytest.mark.asyncio
async def test_get_single_seller(db_session, async_client):
    seller = Seller(
        first_name="Olga", last_name="Buzova",
        email="best_singer@mail.com", password="malo_poloviN!"
    )

    seller2 = Seller(
        first_name="Dasha", last_name="Zoteeva",
        email="instasamka@mail.com", password="Za_dengi_Da!"
    )
    db_session.add_all([seller, seller2])
    await db_session.flush()

    response = await async_client.get(f"/api/v1/sellers/{seller.id}")

    assert response.status_code == status.HTTP_200_OK
    ic(response.json())
    assert response.json() == {
        "first_name": "Olga",
        "last_name": "Buzova",
        "id": seller.id,
        "email": "best_singer@mail.com",
        "books": []
    }

@pytest.mark.asyncio
async def test_get_seller_with_book(db_session, async_client):
    seller = Seller(
        first_name="Olga", last_name="Buzova",
        email="best_singer@mail.com", password="malo_poloviN!"
    )
    db_session.add(seller)
    await db_session.flush()

    book = Book(
        title="How to sing if bear stepped on your ear", 
        author="Buzova Olga", year=2022, pages=7, seller_id=seller.id
        )

    db_session.add(book)
    await db_session.flush()

    response = await async_client.get(f"/api/v1/sellers/{seller.id}")

    assert response.status_code == status.HTTP_200_OK
    ic(response.json())
    assert response.json() == {
        "first_name": "Olga", "last_name": "Buzova", "id": seller.id, 
        "email": "best_singer@mail.com",
        "books": [
            {
                "id": book.id, "seller_id": seller.id,
                "title": "How to sing if bear stepped on your ear", 
                "author": "Buzova Olga", "year": 2022, "pages": 7
            }
        ]
    }

@pytest.mark.asyncio
async def test_delete_seller(db_session, async_client):
    seller = Seller(
        first_name="Olga", last_name="Buzova",
        email="best_singer@mail.com", password="malo_poloviN!"
    )
    db_session.add(seller)
    await db_session.flush()

    response = await async_client.delete(f"/api/v1/sellers/{seller.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    await db_session.flush()
    all_sellers = await db_session.execute(select(Seller))
    res = all_sellers.scalars().all()

    assert len(res) == 0

@pytest.mark.asyncio
async def test_delete_seller_with_invalid_seller_id(db_session, async_client):
    seller = Seller(
        first_name="Olga", last_name="Buzova",
        email="best_singer@mail.com", password="malo_poloviN!"
    )
    db_session.add(seller)
    await db_session.flush()

    response = await async_client.delete(f"/api/v1/sellers/{seller.id + 1}")

    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio
async def test_update_seller(db_session, async_client):
    seller = Seller(
        first_name="Olga", last_name="Buzova",
        email="best_singer@mail.com", password="malo_poloviN!"
    )
    db_session.add(seller)
    await db_session.flush()

    new_seller_data = {
        "id": seller.id, "first_name": "Dasha", "last_name": "Zoteeva",
        "email": "instasamka@mail.com", "password": "Za_dengi_Da!"
    }

    response = await async_client.put(
        f"/api/v1/sellers/{seller.id}", json=new_seller_data
        )

    assert response.status_code == status.HTTP_200_OK
    await db_session.flush()

    res = await db_session.get(Seller, seller.id)

    assert res.first_name == "Dasha"
    assert res.last_name == "Zoteeva"
    assert res.email == "instasamka@mail.com"
    assert res.password == "malo_poloviN!"
    