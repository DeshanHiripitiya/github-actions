from itertools import count

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(title="Minimal FastAPI API")
items: list[dict[str, object]] = []
next_id = count(1)


class ItemCreate(BaseModel):
    name: str
    description: str | None = None


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "FastAPI is running"}


@app.get("/items")
def get_items() -> list[dict[str, object]]:
    return items


@app.post("/items", status_code=201)
def create_item(item: ItemCreate) -> dict[str, object]:
    new_item = {"id": next(next_id), **item.model_dump()}
    items.append(new_item)
    return new_item