from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response
from fastapi import status
from icecream import ic
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.configurations.database import get_async_session
from src.models.books import Book
from src.models.sellers import Seller
from src.schemas import IncomingSeller
from src.schemas import NewSeller
from src.schemas import ReturnedAllSellers
from src.schemas import ReturnedSeller
from src.schemas import SellerBook
from src.schemas import UpdateSeller


sellers_router = APIRouter(
    tags=["sellers"],
    prefix="/sellers",
)

DBSession = Annotated[AsyncSession, Depends(get_async_session)]


@sellers_router.post("/", response_model=NewSeller, status_code=status.HTTP_201_CREATED)
async def create_seller(seller: IncomingSeller, session: DBSession):
    new_seller = Seller(
        first_name=seller.first_name, last_name=seller.last_name,
        email=seller.email, password=seller.get_password(),
    )

    session.add(new_seller)
    await session.flush()

    return new_seller


@sellers_router.get("/", response_model=ReturnedAllSellers)
async def get_all_sellers(session: DBSession):
    query = select(Seller).options(selectinload(Seller.books))
    result = await session.execute(query)
    sellers = result.scalars().all()
    return {"sellers": sellers}


@sellers_router.get("/{seller_id}", response_model=ReturnedSeller)
async def get_seller(seller_id: int, session: DBSession):
    result = await session.get(Seller, seller_id)
    if not result:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    books_result = await session.execute(
        select(Book).where(Book.seller_id == seller_id),
    )

    books = books_result.scalars().all()

    return ReturnedSeller(
        id=result.id,
        first_name=result.first_name,
        last_name=result.last_name,
        email=result.email,
        password=result.password,
        books=[SellerBook.model_validate(book) for book in books],
    )


@sellers_router.delete("/{seller_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_seller(seller_id: int, session: DBSession):
    deleted_seller = await session.get(Seller, seller_id)
    ic(deleted_seller)
    if deleted_seller:
        await session.delete(deleted_seller)
        return None

    return Response(status_code=status.HTTP_404_NOT_FOUND)


@sellers_router.put("/{seller_id}", response_model=UpdateSeller)
async def update_seller(
        seller_id: int, new_seller_data: UpdateSeller, session: DBSession,
):
    if updated_seller := await session.get(Seller, seller_id):
        updated_seller.first_name = new_seller_data.first_name
        updated_seller.last_name = new_seller_data.last_name
        updated_seller.email = new_seller_data.email

        await session.flush()
        return updated_seller

    return Response(status_code=status.HTTP_404_NOT_FOUND)
