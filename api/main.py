from fastapi import FastAPI
from uuid import UUID, uuid4
from typing import List

from api import hero
from api.data_structures import Hero, HeroType
from db.sqlite import SqliteSession

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
    session = SqliteSession()

    hero.create_hero(session, request)

    session.close()

    return request


@app.put("/heroes/{hero_id}", response_model=Hero)
def update_hero(hero_id: UUID, request: Hero):
    updated_hero = hero.update_hero(hero_id, request)

    return updated_hero


@app.delete("/heroes/{hero_id}", response_model=Hero)
def delete_hero(hero_id: UUID):
    deleted_hero = hero.delete_hero(hero_id)

    return TEST_HERO
