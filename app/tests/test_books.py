import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_book():
    author_response = client.post(
        "/authors/", json={"full_name": "Gabriel Garcia Marquez"}
    )
    author_id = author_response.json()["id"]

    book_data = {
        "title": "One Hundred Years of Solitude",
        "author_id": author_id,
        "ISBN": "978-0-06-088328-7",
        "date_published": "1967-05-30",
    }
    response = client.post("/books/", json=book_data)
    assert response.status_code == 201
    assert response.json()["title"] == "One Hundred Years of Solitude"

    book_id = response.json()["id"]
    client.delete(f"/books/{book_id}")
    client.delete(f"/authors/{author_id}")


def test_get_books():
    response = client.get("/books/")
    assert response.status_code in (200, 404)


def test_get_book():
    author_response = client.post("/authors/", json={"full_name": "George Orwell"})
    author_id = author_response.json()["id"]

    book_response = client.post(
        "/books/",
        json={
            "title": "1984",
            "author_id": author_id,
            "ISBN": "978-0-452-28423-4",
            "date_published": "1949-06-08",
        },
    )
    book_id = book_response.json()["id"]

    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "1984"

    client.delete(f"/books/{book_id}")
    client.delete(f"/authors/{author_id}")


def test_update_book():
    author_response = client.post("/authors/", json={"full_name": "Aldous Huxley"})
    author_id = author_response.json()["id"]

    book_response = client.post(
        "/books/",
        json={
            "title": "Brave New World",
            "author_id": author_id,
            "ISBN": "978-0-06-085052-4",
            "date_published": "1932-01-01",
        },
    )
    book_id = book_response.json()["id"]

    update_response = client.put(
        f"/books/{book_id}",
        json={
            "title": "Brave New World (Updated)",
            "author_id": author_id,
            "ISBN": "978-0-06-085052-4",
            "date_published": "1932-01-01",
        },
    )
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Brave New World (Updated)"

    client.delete(f"/books/{book_id}")
    client.delete(f"/authors/{author_id}")


def test_delete_book():
    author_response = client.post(
        "/authors/", json={"full_name": "F. Scott Fitzgerald"}
    )
    author_id = author_response.json()["id"]

    book_response = client.post(
        "/books/",
        json={
            "title": "The Great Gatsby",
            "author_id": author_id,
            "ISBN": "978-0-7432-7356-5",
            "date_published": "1925-04-10",
        },
    )
    book_id = book_response.json()["id"]

    delete_response = client.delete(f"/books/{book_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/books/{book_id}")
    assert get_response.status_code == 404

    client.delete(f"/authors/{author_id}")


def test_search_books():
    author_response = client.post("/authors/", json={"full_name": "Isaac Asimov"})
    author_id = author_response.json()["id"]

    book_response = client.post(
        "/books/",
        json={
            "title": "Foundation",
            "author_id": author_id,
            "ISBN": "978-0-553-80371-0",
            "date_published": "1951-06-01",
        },
    )
    book_id = book_response.json()["id"]

    search_response = client.get("/books/search/", params={"author_name": "Asimov"})
    assert search_response.status_code == 200
    assert len(search_response.json()) > 0

    client.delete(f"/books/{book_id}")
    client.delete(f"/authors/{author_id}")
