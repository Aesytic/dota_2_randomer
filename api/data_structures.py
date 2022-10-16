import json
from pydantic import BaseModel
from enum import Enum
from uuid import UUID
from typing import Optional


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
    hero_type: HeroType


# The fields of this model should remain aligned with the fields in the Hero model
class HeroUpdateRequest(BaseSerialisableModel):
    name: Optional[str] = None
    randomable: Optional[bool] = None
    hero_type: Optional[HeroType] = None
