import pytest
from fastapi.testclient import TestClient

from app import app, items


@pytest.fixture(autouse=True)
def clear_items() -> None:
    items.clear()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_read_root(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "FastAPI is running"}


def test_get_items_returns_empty_list(client: TestClient) -> None:
    response = client.get("/items")

    assert response.status_code == 200
    assert response.json() == []


def test_create_item(client: TestClient) -> None:
    response = client.post(
        "/items",
        json={"name": "First item", "description": "Test description"},
    )

    assert response.status_code == 201
    created_item = response.json()
    assert isinstance(created_item["id"], int)
    assert created_item["name"] == "First item"
    assert created_item["description"] == "Test description"


def test_created_item_is_returned_by_get_items(client: TestClient) -> None:
    client.post("/items", json={"name": "Saved item"})

    response = client.get("/items")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Saved item"
    assert response.json()[0]["description"] is None


def test_create_item_requires_name(client: TestClient) -> None:
    response = client.post("/items", json={"description": "Missing name"})

    assert response.status_code == 422