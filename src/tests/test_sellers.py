import pytest
from fastapi import status
from sqlalchemy import select
from src.models.sellers import Seller
from src.models.books import Book
from icecream import ic

@pytest.mark.asyncio
async def test_create_seller(async_client):
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "e_mail": "john.doe@example.com",
        "password": "secret123"
    }
    response = await async_client.post("/api/v1/seller/", json=data)
    assert response.status_code == status.HTTP_201_CREATED

    result_data = response.json()
    seller_id = result_data.pop("id", None)
    assert seller_id, "Seller id not returned from endpoint"
    assert result_data == {
        "first_name": "John",
        "last_name": "Doe",
        "e_mail": "john.doe@example.com"
    }

@pytest.mark.asyncio
async def test_get_all_sellers(db_session, async_client):
    seller1 = Seller(first_name="Alice", last_name="Smith", e_mail="alice@example.com", password="pass1")
    seller2 = Seller(first_name="Bob", last_name="Johnson", e_mail="bob@example.com", password="pass2")
    db_session.add_all([seller1, seller2])
    await db_session.flush()

    response = await async_client.get("/api/v1/seller/")
    assert response.status_code == status.HTTP_200_OK

    sellers = response.json()
    assert len(sellers) >= 2
    
    emails = [seller["e_mail"] for seller in sellers]
    assert "alice@example.com" in emails
    assert "bob@example.com" in emails


@pytest.mark.asyncio
async def test_get_single_seller(db_session, async_client):
    
    seller = Seller(first_name="Charlie", last_name="Brown", e_mail="charlie@example.com", password="pass3")
    db_session.add(seller)
    await db_session.flush()

    response = await async_client.get(f"/api/v1/seller/{seller.id}")
    assert response.status_code == status.HTTP_200_OK

    assert response.json() == {
        "id": seller.id,
        "first_name": "Charlie",
        "last_name": "Brown",
        "e_mail": "charlie@example.com",
        "books": []
    }


@pytest.mark.asyncio
async def test_update_seller(db_session, async_client):
    seller = Seller(first_name="David", last_name="Miller", e_mail="david@example.com", password="pass4")
    db_session.add(seller)
    await db_session.flush()

    update_data = {
        "first_name": "Dave",
        "last_name": "Mills",
        "e_mail": "dave.mills@example.com"
    }
    response = await async_client.put(f"/api/v1/seller/{seller.id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK

    result = response.json()
    assert result["first_name"] == "Dave"
    assert result["last_name"] == "Mills"
    assert result["e_mail"] == "dave.mills@example.com"
    assert result["id"] == seller.id


@pytest.mark.asyncio
async def test_delete_seller(db_session, async_client):
    seller = Seller(first_name="Eve", last_name="Adams", e_mail="eve@example.com", password="pass5")
    db_session.add(seller)
    await db_session.flush()
    ic(seller.id)

    response = await async_client.delete(f"/api/v1/seller/{seller.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    await db_session.flush()
    result = await db_session.execute(select(Seller).where(Seller.id == seller.id))
    seller_in_db = result.scalars().first()
    assert seller_in_db is None


@pytest.mark.asyncio
async def test_get_seller_with_books(db_session, async_client):
    seller = Seller(first_name="Fiona", last_name="Green", e_mail="fiona@example.com", password="pass6")
    book1 = Book(title="Book One", author="Author One", year=2025, pages=123)
    book2 = Book(title="Book Two", author="Author Two", year=2025, pages=456)
    seller.books = [book1, book2]
    db_session.add(seller)
    await db_session.flush()

    response = await async_client.get(f"/api/v1/seller/{seller.id}")
    assert response.status_code == status.HTTP_200_OK

    expected_books = [
        {"id": book1.id, "title": book1.title, "author": book1.author, "year": book1.year, "count_pages": book1.pages},
        {"id": book2.id, "title": book2.title, "author": book2.author, "year": book2.year, "count_pages": book2.pages},
    ]
    assert response.json() == {
        "id": seller.id,
        "first_name": seller.first_name,
        "last_name": seller.last_name,
        "e_mail": seller.e_mail,
        "books": expected_books,
    }