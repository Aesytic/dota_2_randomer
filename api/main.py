from fastapi import FastAPI, HTTPException
from uuid import UUID, uuid4
from typing import List

from api import hero
from api.data_structures import Hero, HeroType, HeroUpdateRequest
from db.sqlite import engine_factory, sessionmaker_factory

app = FastAPI()

engine = engine_factory()
sessionmaker = sessionmaker_factory(engine)

TEST_HERO = Hero(id=uuid4(), name="testing", randomable=True, hero_type=HeroType.MID)


@app.get("/")
def index():
    return {"Hello": "World"}


@app.get("/random/hero", response_model=Hero)
def random_hero():
    session = sessionmaker()

    with session.begin():
        try:
            randomed_hero = hero.get_random_hero(session)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    return randomed_hero


@app.get("/heroes", response_model=List[Hero])
def list_heroes():
    session = sessionmaker()

    with session.begin():
        all_heroes = hero.read_all_heroes(session)

    return all_heroes


@app.get("/heroes/{hero_name}", response_model=Hero)
def read_hero_from_name(hero_name: str):
    session = sessionmaker()

    with session.begin():
        try:
            queried_hero = hero.read_hero(session, hero_name)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    return queried_hero


@app.post("/heroes")
def create_hero(request: Hero):
    session = sessionmaker()

    with session.begin():
        created_hero = hero.create_hero(session, request)

    return created_hero


@app.put("/heroes/{hero_id}", response_model=Hero)
def update_hero(hero_id: UUID, request: HeroUpdateRequest):
    session = sessionmaker()

    with session.begin():
        try:
            updated_hero = hero.update_hero(session, hero_id, request)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    return updated_hero


@app.delete("/heroes/{hero_id}", response_model=Hero)
def delete_hero(hero_id: UUID):
    session = sessionmaker()

    with session.begin():
        try:
            deleted_hero = hero.delete_hero(session, hero_id)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    return deleted_hero
