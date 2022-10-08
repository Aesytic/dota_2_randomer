import json
from pydantic import BaseModel
from enum import Enum
from uuid import UUID


class BaseSerialisableModel(BaseModel):
    def to_dict(self):
        return json.loads(self.json())


class HeroType(Enum):
    CARRY = "carry"
    MID = "mid"
    OFFLANE = "offlane"
    SUPPORT = "support"


class Hero(BaseSerialisableModel):
    id: UUID
    name: str
    randomable: bool = True
    hero_type: HeroType
