from fastapi import FastAPI
from uuid import UUID, uuid4
from typing import List

from api.data_structures import Hero, HeroType
from api.hero import add_hero, update_hero, delete_hero

app = FastAPI()

TEST_HERO = Hero(id=uuid4(), name="testing", randomable=True, hero_type=HeroType.MID)


@app.get("/")
def index():
    return {"Hello": "World"}


@app.get("/heroes", response_model=List[Hero])
def list_heroes():
    return [TEST_HERO]


@app.get("/heroes/{hero_id}", response_model=Hero)
def read_hero(hero_id: UUID):
    return TEST_HERO


@app.post("/heroes")
def create_hero(request: Hero):
    add_hero(request)

    return request


@app.put("/heroes/{hero_id}", response_model=Hero)
def update_hero(hero_id: UUID, request: Hero):
    updated_hero = update_hero(hero_id, request)

    return updated_hero


@app.delete("/heroes/{hero_id}", response_model=Hero)
def delete_hero(hero_id: UUID):
    deleted_hero = delete_hero(hero_id)

    return TEST_HERO
