from typing import Annotated
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import select
from src.models.sellers import Seller
from sqlalchemy.orm import selectinload
from src.schemas import (
    RegisteringSeller, ReturnedSeller, ReturnedSellerWithBooks,
    ReturnedAllSellers,
)
from icecream import ic
from sqlalchemy.ext.asyncio import AsyncSession
from src.configurations import get_async_session

seller_router = APIRouter(tags=["seller"], prefix="/seller")

DBSession = Annotated[AsyncSession, Depends(get_async_session)]


@seller_router.post(
    '', response_model=ReturnedSeller, status_code=status.HTTP_201_CREATED
)
async def register_seller(seller: RegisteringSeller, session: DBSession):
    new_seller = Seller(
        **{
            'first_name': seller.first_name,
            'last_name': seller.last_name,
            'e_mail': seller.e_mail,
            'password': seller.password,
        }
    )

    session.add(new_seller)
    await session.flush()

    return new_seller


@seller_router.get('', response_model=ReturnedAllSellers)
async def get_all_sellers(session: DBSession):
    query = select(Seller)
    result = await session.execute(query)
    sellers = result.scalars().all()
    return {'sellers': sellers}


@seller_router.get('/{seller_id}', response_model=ReturnedSellerWithBooks)
async def get_seller(seller_id: int, session: DBSession):
    result = await session.execute(
        select(Seller).options(selectinload(Seller.books)).where(Seller.id == seller_id)
    )
    seller = result.scalar_one_or_none()
    if seller:
        return seller
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    

@seller_router.put('/{seller_id}', response_model=ReturnedSeller)
async def update_seller(seller_id: int, new_seller_data: ReturnedSeller, session: DBSession):
    if updated_seller := await session.get(Seller, seller_id):
        updated_seller.first_name = new_seller_data.first_name
        updated_seller.last_name = new_seller_data.last_name
        updated_seller.e_mail = new_seller_data.e_mail

        await session.flush()
        
        return updated_seller
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@seller_router.delete('/{seller_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_seller(seller_id: int, session: DBSession):
    deleted_seller = await session.get(Seller, seller_id)
    ic(deleted_seller)
    if deleted_seller:
        await session.delete(deleted_seller)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
