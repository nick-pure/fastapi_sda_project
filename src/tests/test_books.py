import pytest
from sqlalchemy import select
from src.models.books import Book
from src.models.sellers import Seller
from fastapi import status
from icecream import ic
from .data import *

@pytest.mark.asyncio
async def test_create_book(db_session, async_client):
    seller = Seller(**seller1)
    db_session.add(seller)
    await db_session.flush()

    book = book1.copy()
    book['seller_id'] = seller.id
    response = await async_client.post("/api/v1/books/", json=book)

    assert response.status_code == status.HTTP_201_CREATED

    result_data = response.json()

    resp_book_id = result_data.pop("id", None)
    assert resp_book_id, "The book id was not returned from the endpoint"

    right_result_data = make_returned(book)

    assert result_data == right_result_data


@pytest.mark.asyncio
async def test_create_book_with_old_year(async_client):
    book = book1.copy()
    book['year'] = 1985 # < 2020
    response = await async_client.post("/api/v1/books/", json=book)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_get_books(db_session, async_client):
    seller = Seller(**seller1)
    db_session.add(seller)
    await db_session.flush()

    books = [make_returned(book1), make_returned(book2)]
    books[0]['seller_id'] = seller.id
    books[1]['seller_id'] = seller.id
    added_books = [Book(**books[0]), Book(**books[1])]

    db_session.add_all(added_books)
    await db_session.flush()

    response = await async_client.get("/api/v1/books/")

    assert response.status_code == status.HTTP_200_OK

    result_data = response.json()
    assert len(result_data["books"]) == 2

    right_result_data = books.copy()
    right_result_data[0]['id'] = added_books[0].id
    right_result_data[1]['id'] = added_books[1].id
    assert result_data['books'] == right_result_data


@pytest.mark.asyncio
async def test_get_single_book(db_session, async_client):
    seller = Seller(**seller1)
    db_session.add(seller)
    await db_session.flush()

    books = [make_returned(book1), make_returned(book2)]
    books[0]['seller_id'] = seller.id
    books[1]['seller_id'] = seller.id
    added_books = [Book(**books[0]), Book(**books[1])]

    db_session.add_all(added_books)
    await db_session.flush()

    response = await async_client.get(f"/api/v1/books/{added_books[0].id}")

    assert response.status_code == status.HTTP_200_OK

    right_result_data = books[0]
    right_result_data['id'] = added_books[0].id

    assert response.json() == right_result_data


@pytest.mark.asyncio
async def test_update_book(db_session, async_client):
    seller = Seller(**seller1)
    db_session.add(seller)
    await db_session.flush()

    book = make_returned(book1)
    book['seller_id'] = seller.id
    added_book = Book(**book)
    db_session.add(added_book)
    await db_session.flush()

    updated_book = make_returned(book2)
    updated_book['seller_id'] = seller.id
    updated_book['id'] = added_book.id
    response = await async_client.put(
        f"/api/v1/books/{added_book.id}",
        json=updated_book,
    )

    assert response.status_code == status.HTTP_200_OK
    await db_session.flush()

    res = await db_session.get(Book, added_book.id)
    assert res.title == updated_book['title']
    assert res.author == updated_book['author']
    assert res.pages == updated_book['pages']
    assert res.year == updated_book['year']
    assert res.id == updated_book['id']


@pytest.mark.asyncio
async def test_delete_book(db_session, async_client):
    lenght_before = len((await db_session.execute(select(Book))).scalars().all())

    seller = Seller(**seller1)
    db_session.add(seller)
    await db_session.flush()

    book = make_returned(book1)
    book['seller_id'] = seller.id
    added_book = Book(**book)
    db_session.add(added_book)
    await db_session.flush()

    response = await async_client.delete(f"/api/v1/books/{added_book.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    await db_session.flush()
    lenght_after = len((await db_session.execute(select(Book))).scalars().all())

    assert lenght_after == lenght_before


@pytest.mark.asyncio
async def test_delete_book_with_invalid_book_id(db_session, async_client):
    seller = Seller(**seller1)
    db_session.add(seller)
    await db_session.flush()

    book = make_returned(book1)
    book['seller_id'] = seller.id
    added_book = Book(**book)
    db_session.add(added_book)
    await db_session.flush()

    response = await async_client.delete(f"/api/v1/books/{added_book.id + 1}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
