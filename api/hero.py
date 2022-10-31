from uuid import UUID
from sqlalchemy.orm import Session, Query
from typing import List
import random

from api.data_structures import Hero, HeroUpdateRequest
from db import models


def read_all_heroes(session: Session, id: str, name: str, randomable: bool, hero_type: str) -> List[Hero]:
    db_query = session.query(models.Heroes)

    # Filter in order of most restrictive to least restrictive
    if id:
        db_query = db_query.filter(models.Heroes.id == id)

    if name:
        db_query = db_query.filter(models.Heroes.name == name)

    if randomable is not None:
        db_query = db_query.filter(models.Heroes.randomable == randomable)

    if hero_type:
        db_query = db_query.filter(models.Heroes.hero_type == hero_type)

    hero_rows = db_query.all()

    return [Hero.from_hero_db_model(hero_row) for hero_row in hero_rows]


def create_hero(session: Session, hero: Hero) -> Hero:
    hero_row = models.Heroes(**hero.to_dict())
    session.add(hero_row)
    session.commit()

    return hero


def read_hero(session: Session, hero_id: str) -> Hero:
    hero_row = session.query(models.Heroes).filter(models.Heroes.id == hero_id).first()

    if hero_row is None:
        raise ValueError(f"Hero {hero_id} not found")

    return Hero.from_hero_db_model(hero_row)


def update_hero(session: Session, hero_id: UUID, update_hero_request: HeroUpdateRequest) -> Hero:
    hero_row = session.query(models.Heroes).filter(models.Heroes.id == str(hero_id)).first()

    if hero_row is None:
        raise ValueError(f"Hero ID {hero_id} not found")

    if update_hero_request.name is not None:
        hero_row.name = update_hero_request.name

    if update_hero_request.randomable is not None:
        hero_row.randomable = update_hero_request.randomable

    if update_hero_request.hero_type is not None:
        hero_row.hero_type = update_hero_request.hero_type.value

    updated_hero = Hero.from_hero_db_model(hero_row)
    session.commit()

    return updated_hero


def delete_hero(session: Session, hero_id: UUID):
    hero_row = session.query(models.Heroes).filter(models.Heroes.id == str(hero_id)).first()

    if hero_row is None:
        raise ValueError(f"Hero ID {hero_id} not found")

    deleted_hero = Hero.from_hero_db_model(hero_row)

    session.delete(hero_row)
    session.commit()

    return deleted_hero


def get_random_hero(session: Session) -> Hero:
    # TODO: use more efficient approach to get a random hero
    # Should be fine now as there are unlikely to ever be more than 200 heroes
    randomable_heroes = session.query(models.Heroes).filter(models.Heroes.randomable == True).all()
    num_randomable_heroes = len(randomable_heroes)

    if num_randomable_heroes == 0:
        raise ValueError("No randomable heroes in DB")

    return Hero.from_hero_db_model(randomable_heroes[random.randrange(0, num_randomable_heroes)])
