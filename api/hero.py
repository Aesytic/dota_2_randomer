from uuid import UUID
from sqlalchemy.orm import Session
from typing import List
import random

from api.data_structures import Hero, HeroUpdateRequest
from db import models


def read_all_heroes(session: Session) -> List[Hero]:
    hero_rows = session.query(models.Heroes).all()

    return [Hero.from_hero_db_model(hero_row) for hero_row in hero_rows]


def create_hero(session: Session, hero: Hero) -> Hero:
    hero_row = models.Heroes(**hero.to_dict())
    session.add(hero_row)
    session.commit()

    return hero


def read_hero(session: Session, hero_name: str) -> Hero:
    hero_row = session.query(models.Heroes).filter(models.Heroes.name == hero_name).first()

    if hero_row is None:
        raise ValueError(f"Hero {hero_name} not found")

    return Hero.from_hero_db_model(hero_row)


def update_hero(session: Session, hero_id: UUID, updated_hero: HeroUpdateRequest) -> Hero:
    hero_row = session.query(models.Heroes).filter(models.Heroes.id == str(hero_id)).first()

    if hero_row is None:
        raise ValueError(f"Hero ID {hero_id} not found")

    if updated_hero.name is not None:
        hero_row.name = updated_hero.name

    if updated_hero.randomable is not None:
        hero_row.randomable = updated_hero.randomable

    if updated_hero.hero_type is not None:
        hero_row.hero_type = updated_hero.hero_type.value

    session.commit()

    return Hero.from_hero_db_model(hero_row)


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
