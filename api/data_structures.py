from pydantic import BaseModel
from enum import Enum
from uuid import UUID


class HeroType(Enum):
    CARRY = "carry"
    MID = "mid"
    OFFLANE = "offlane"
    SUPPORT = "support"


class Hero(BaseModel):
    id: UUID
    name: str
    randomable: bool = True
    hero_type: HeroType
