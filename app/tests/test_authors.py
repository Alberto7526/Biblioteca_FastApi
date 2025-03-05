import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_create_author():
    response = client.post("/authors/", json={"full_name": "J.K. Rowling"})
    assert response.status_code == 201
    assert response.json()["full_name"] == "J.K. Rowling"

    author_id = response.json()["id"]
    client.delete(f"/authors/{author_id}")


def test_get_authors():
    response = client.get("/authors/")
    assert response.status_code in (200, 404)


def test_get_author():
    create_response = client.post("/authors/", json={"full_name": "George Orwell"})
    author_id = create_response.json()["id"]
    response = client.get(f"/authors/{author_id}")
    assert response.status_code == 200
    assert response.json()["full_name"] == "George Orwell"

    client.delete(f"/authors/{author_id}")


def test_update_author():
    create_response = client.post("/authors/", json={"full_name": "Ernest Hemingway"})
    author_id = create_response.json()["id"]

    update_response = client.put(
        f"/authors/{author_id}", json={"full_name": "Hemingway"}
    )
    assert update_response.status_code == 200
    assert update_response.json()["full_name"] == "Hemingway"

    client.delete(f"/authors/{author_id}")


def test_delete_author():
    create_response = client.post(
        "/authors/", json={"full_name": "F. Scott Fitzgerald"}
    )
    author_id = create_response.json()["id"]

    delete_response = client.delete(f"/authors/{author_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/authors/{author_id}")
    assert get_response.status_code == 404
