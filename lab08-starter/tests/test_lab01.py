"""LAB 1 — add your five tests here. Do not delete the smoke tests.

A. GET /books, empty database -> HTTP 200 and []
B. GET /books/9999 -> HTTP 404, JSON code == NOT_FOUND
C. POST /books with only author -> HTTP 400, errors contains title
D. POST valid book, DELETE it, GET same id -> HTTP 404
BONUS. Validate a Book response using JSON Schema; add an unknown
       field to a *copy* of the response and assert ValidationError.

Useful imports:
    from jsonschema import validate, ValidationError
    import pytest
    from tools import get_book_schema

Do not depend on test execution order. Fixtures: client, app, sample_book.
"""


def test_get_books_empty_database(client):
    response = client.get("/books")

    assert response.status_code == 200
    assert response.get_json() == []


def test_get_missing_book_returns_not_found(client):
    response = client.get("/books/9999")

    assert response.status_code == 404
    assert response.get_json()["code"] == "NOT_FOUND"


def test_create_book_without_title_returns_validation_error(client):
    response = client.post("/books", json={"author": "J.J. Geewax"})

    assert response.status_code == 400
    assert any(error["field"] == "title" for error in response.get_json()["errors"])


def test_deleted_book_cannot_be_fetched(client, sample_book):
    delete_response = client.delete(f"/books/{sample_book}")

    assert delete_response.status_code == 204

    get_response = client.get(f"/books/{sample_book}")

    assert get_response.status_code == 404
