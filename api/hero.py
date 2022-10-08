from uuid import UUID
from sqlalchemy.orm import Session

from api.data_structures import Hero
from db import models


def create_hero(session: Session, hero: Hero):
    hero_row = models.Heroes(**hero.to_dict())
    session.add(hero_row)
    session.commit()


def update_hero(hero_id: UUID, hero: Hero):
    return hero


def delete_hero(hero_id: UUID):
    return None
