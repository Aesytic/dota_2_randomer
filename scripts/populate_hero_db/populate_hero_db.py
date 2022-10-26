import sys
import os
import os.path
from pathlib import Path
import requests
from typing import List
from pydantic import BaseModel
from uuid import uuid4

sys.path.append(os.path.join(Path(__file__).parent, os.pardir, os.pardir))

from scripts.api_client import ApiClient
from api.data_structures import Hero, HeroType


HEROES_API = "https://api.opendota.com/api/heroes"


class OpenDotaHeroModel(BaseModel):
    id: int
    name: str
    localized_name: str
    primary_attr: str
    attack_type: str
    roles: List[str]
    legs: int  # Note that this is not documented in the API


class OpenDotaHeroesResponse(BaseModel):
    # Refer to https://docs.opendota.com/#tag/heroes%2Fpaths%2F~1heroes%2Fget for API spec
    response: List[OpenDotaHeroModel]


def main():
    if len(sys.argv) != 2:
        sys.exit(f"Usage: python {sys.argv[0]} <API base URL>")

    load_heroes(api_base_url=sys.argv[1])


def load_heroes(api_base_url: str):
    hero_randomiser_api_client = ApiClient(base_url=api_base_url)

    heroes_response = requests.get(HEROES_API)
    heroes = OpenDotaHeroesResponse(response=heroes_response.json())

    for hero in heroes.response:
        if check_hero_exists(hero_randomiser_api_client, hero.localized_name):
            print(f"Hero {hero.localized_name} already exists - skipping")
            continue

        hero_id = uuid4()
        # Find first enum-compatible role in API - note that the HeroType enum is a subset of the roles from the
        #   OpenDota API
        # Otherwise default to support
        hero_type = HeroType.SUPPORT.value
        for role in hero.roles:
            try:
                hero_type = HeroType(role).value
            except ValueError:
                continue
            else:
                break

        hero = Hero(id=str(hero_id), name=hero.localized_name, hero_type=hero_type)
        hero_randomiser_api_client.post("/heroes", hero.json())

        print(f"Added {hero}")


def check_hero_exists(hero_randomiser_api_client: ApiClient, hero_name: str) -> bool:
    hero_name_query = hero_randomiser_api_client.get(f"/heroes/{hero_name}")

    if hero_name_query.status_code == 404:
        return False

    return True


if __name__ == "__main__":
    main()
