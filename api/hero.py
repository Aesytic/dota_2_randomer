from uuid import UUID
from sqlalchemy.orm import Session

from api.data_structures import Hero, HeroType, HeroUpdateRequest
from db import models


def create_hero(session: Session, hero: Hero) -> Hero:
    hero_row = models.Heroes(**hero.to_dict())
    session.add(hero_row)
    session.commit()

    return hero


def read_hero(session: Session, hero_id: UUID) -> Hero:
    hero_row = session.query(models.Heroes).filter(models.Heroes.id == str(hero_id)).first()

    if hero_row is None:
        raise ValueError(f"Hero ID {hero_id} not found")

    return hero_row_to_base_model(hero_row)



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

    return hero_row_to_base_model(hero_row)


def delete_hero(hero_id: UUID):
    return None


def hero_row_to_base_model(hero_row: models.Heroes) -> Hero:
    return Hero(id=hero_row.id, name=hero_row.name, randomable=hero_row.randomable, hero_type=HeroType(hero_row.hero_type))
