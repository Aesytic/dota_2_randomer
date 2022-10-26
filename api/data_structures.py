import json
from pydantic import BaseModel
from enum import Enum
from uuid import UUID
from typing import Optional

from db.models import Heroes


class BaseSerialisableModel(BaseModel):
    def to_dict(self):
        return json.loads(self.json())


class HeroType(Enum):
    CARRY = "carry"
    MID = "mid"
    OFFLANE = "offlane"
    SUPPORT = "support"


# The fields of this model should remain aligned with the fields in the DB Heroes model
# The fields of this model should remain aligned with the fields in the HeroUpdateRequest model (excluding id)
class Hero(BaseSerialisableModel):
    id: UUID
    name: str
    randomable: bool = True
    hero_type: HeroType  # TODO: Support multiple hero types for a hero

    @classmethod
    def from_hero_db_model(cls, hero_row: Heroes):
        return cls(id=hero_row.id,
                   name=hero_row.name,
                   randomable=hero_row.randomable,
                   hero_type=HeroType(hero_row.hero_type))


# The fields of this model should remain aligned with the fields in the Hero model
class HeroUpdateRequest(BaseSerialisableModel):
    name: Optional[str] = None
    randomable: Optional[bool] = None
    hero_type: Optional[HeroType] = None
