from typing import Annotated, List
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.configurations.database import get_async_session
from src.models.sellers import Seller
from src.schemas.sellers import SellerCreate, SellerUpdate, SellerOut, SellerOutWithBooks

sellers_router = APIRouter(tags=["seller"], prefix="/seller")

DBSession = Annotated[AsyncSession, Depends(get_async_session)]

@sellers_router.post("/", response_model=SellerOut, status_code=status.HTTP_201_CREATED)
async def create_seller(seller: SellerCreate, session: DBSession):
    new_seller = Seller(
        first_name=seller.first_name,
        last_name=seller.last_name,
        e_mail=seller.e_mail,
        password=seller.password
    )
    session.add(new_seller)
    await session.flush()
    return new_seller

@sellers_router.get("/", response_model=List[SellerOut])
async def get_all_sellers(session: DBSession):
    result = await session.execute(select(Seller))
    sellers = result.scalars().all()
    return sellers

@sellers_router.get("/{seller_id}", response_model=SellerOutWithBooks)
async def get_seller(seller_id: int, session: DBSession):
    query = (
        select(Seller)
        .options(selectinload(Seller.books))
        .filter(Seller.id == seller_id)
    )
    result = await session.execute(query)
    seller = result.scalars().first()

    if seller:
        return seller

    return Response(status_code=status.HTTP_404_NOT_FOUND)

@sellers_router.put("/{seller_id}", response_model=SellerOut)
async def update_seller(seller_id: int, seller_update: SellerUpdate, session: DBSession):
    seller = await session.get(Seller, seller_id)
    if seller:
        if seller_update.first_name is not None:
            seller.first_name = seller_update.first_name
        if seller_update.last_name is not None:
            seller.last_name = seller_update.last_name
        if seller_update.e_mail is not None:
            seller.e_mail = seller_update.e_mail
        await session.flush()
        return seller
    return Response(status_code=status.HTTP_404_NOT_FOUND)

@sellers_router.delete("/{seller_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_seller(seller_id: int, session: DBSession):
    seller = await session.get(Seller, seller_id)
    if seller:
        await session.delete(seller)
        await session.flush()
        return
    return Response(status_code=status.HTTP_404_NOT_FOUND)
