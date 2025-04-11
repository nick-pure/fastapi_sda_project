import pytest
from sqlalchemy import select
from src.models.books import Book
from src.models.sellers import Seller
from fastapi import status
from icecream import ic
from .data import *

@pytest.mark.asyncio
async def test_create_seller(async_client):
    seller = seller1.copy()
    response = await async_client.post("/api/v1/seller", json=seller)
    assert response.status_code == status.HTTP_201_CREATED

    result_data = response.json()

    resp_seller_id = result_data.pop("id", None)
    assert resp_seller_id, "The seller id was not returned from the endpoint"

    right_result_data = seller.copy()
    right_result_data.pop('password')

    assert result_data == right_result_data

@pytest.mark.asyncio
async def test_create_seller_with_weak_password(async_client):
    seller = seller1.copy()
    seller['password'] = '12345678'
    response = await async_client.post("/api/v1/seller", json=seller)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_create_seller_with_wrong_email(async_client):
    seller = seller1.copy()
    seller['e_mail'] = 'not_email'
    response = await async_client.post("/api/v1/seller", json=seller)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_get_all_sellers(db_session, async_client):
    sellers = [seller1.copy(), seller2.copy()]
    added_sellers = [Seller(**sellers[0]), Seller(**sellers[1])]
    db_session.add_all(added_sellers)
    await db_session.flush()

    response = await async_client.get("/api/v1/seller")
    assert response.status_code == status.HTTP_200_OK

    result_data = response.json()
    assert len(result_data['sellers']) == 2

    right_result_data = sellers.copy()
    right_result_data[0].pop('password')
    right_result_data[1].pop('password')
    right_result_data[0]['id'] = added_sellers[0].id
    right_result_data[1]['id'] = added_sellers[1].id

    assert result_data['sellers'] == right_result_data

@pytest.mark.asyncio
async def test_get_single_seller(db_session, async_client):
    seller = seller1.copy()
    added_seller = Seller(**seller)
    another_seller = Seller(**seller2)

    db_session.add_all([added_seller, another_seller])
    await db_session.flush()

    books = [make_returned(book1), make_returned(book2)]
    books[0]['seller_id'] = added_seller.id
    books[1]['seller_id'] = added_seller.id
    added_books = [Book(**books[0]), Book(**books[1])]

    db_session.add_all(added_books)
    await db_session.flush()

    response = await async_client.get(f"/api/v1/seller/{added_seller.id}")

    assert response.status_code == status.HTTP_200_OK

    result_data = response.json()
    right_books_of_sellers = [make_incoming(books[0]), make_incoming(books[1])]
    right_books_of_sellers[0]['id'] = added_books[0].id
    right_books_of_sellers[1]['id'] = added_books[1].id
    for book in right_books_of_sellers:
        book.pop('seller_id')

    assert result_data['books'] == right_books_of_sellers
    result_data.pop('books')

    right_seller = seller.copy()
    right_seller.pop('password')
    right_seller['email'] = right_seller['e_mail']
    right_seller.pop('e_mail')
    right_seller['id'] = added_seller.id

    assert result_data == right_seller


@pytest.mark.asyncio
async def test_update_seller(db_session, async_client):
    seller = Seller(**seller1)
    db_session.add(seller)
    await db_session.flush()

    updated_seller = seller2.copy()
    updated_seller['id'] = seller.id
    response = await async_client.put(
        f"/api/v1/seller/{seller.id}",
        json=updated_seller,
    )
    assert response.status_code == status.HTTP_200_OK
    await db_session.flush()

    res = await db_session.get(Seller, seller.id)
    assert res.first_name == updated_seller['first_name']
    assert res.last_name == updated_seller['last_name']
    assert res.e_mail == updated_seller['e_mail']
    assert res.id == updated_seller['id']

@pytest.mark.asyncio
async def test_update_sellers_password(db_session, async_client):
    seller = seller1.copy()
    seller['password'] = 'Orange1_3'
    added_seller = Seller(**seller)
    db_session.add(added_seller)
    await db_session.flush()

    updated_seller = seller2.copy()
    updated_seller['id'] = added_seller.id
    response = await async_client.put(
        f"/api/v1/seller/{added_seller.id}",
        json=updated_seller,
    )
    assert response.status_code == status.HTTP_200_OK
    await db_session.flush()

    res = await db_session.get(Seller, added_seller.id)
    assert res.first_name == updated_seller['first_name']
    assert res.last_name == updated_seller['last_name']
    assert res.e_mail == updated_seller['e_mail']
    assert res.id == updated_seller['id']
    assert res.password != updated_seller['password']


@pytest.mark.asyncio
async def test_delete_seller(db_session, async_client):
    seller_lenght_before = len((await db_session.execute(select(Seller))).scalars().all())
    book_lenght_before = len((await db_session.execute(select(Book))).scalars().all())

    seller = seller1.copy()
    added_seller = Seller(**seller)

    db_session.add(added_seller)
    await db_session.flush()

    books = [make_returned(book1), make_returned(book2)]
    books[0]['seller_id'] = added_seller.id
    books[1]['seller_id'] = added_seller.id
    added_books = [Book(**books[0]), Book(**books[1])]

    db_session.add_all(added_books)
    await db_session.flush()

    response = await async_client.delete(f"/api/v1/seller/{added_seller.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    await db_session.flush()
    seller_lenght_after = len((await db_session.execute(select(Seller))).scalars().all())
    book_lenght_after = len((await db_session.execute(select(Book))).scalars().all())

    assert seller_lenght_after == seller_lenght_before
    assert book_lenght_after == book_lenght_before


@pytest.mark.asyncio
async def test_delete_seller_with_invalid_seller_id(db_session, async_client):
    seller = seller1.copy()
    added_seller = Seller(**seller)

    db_session.add(added_seller)
    await db_session.flush()

    books = [make_returned(book1), make_returned(book2)]
    books[0]['seller_id'] = added_seller.id
    books[1]['seller_id'] = added_seller.id
    added_books = [Book(**books[0]), Book(**books[1])]

    db_session.add_all(added_books)
    await db_session.flush()

    response = await async_client.delete(f"/api/v1/seller/{added_seller.id + 1}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
