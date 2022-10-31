import sys
import os
import os.path
from pathlib import Path
from typing import List, Optional

sys.path.append(os.path.join(Path(__file__).parent, os.pardir, os.pardir))

from scripts.api_client import ApiClient
from api.data_structures import Hero, HeroType


def get_all_heroes(hero_randomiser_api_client: ApiClient) -> List[Hero]:
    get_heroes_response = hero_randomiser_api_client.get("/heroes")

    return [Hero(**hero) for hero in get_heroes_response.json()]


def get_hero(hero_randomiser_api_client: ApiClient, hero_name: str) -> List[Hero]:
    hero_response = hero_randomiser_api_client.get(f"/heroes?name={hero_name}")

    if hero_response.status_code != 200:
        error_message = hero_response.json()["detail"]
        raise ValueError(error_message)

    return [Hero(**hero) for hero in hero_response.json()]


def main(api_base_url: str, hero_name: Optional[str] = None):
    hero_randomiser_api_client = ApiClient(base_url=api_base_url)
    if hero_name:
        try:
            hero_list = get_hero(hero_randomiser_api_client, hero_name)
        except Exception as e:
            print(f"Error while querying {hero_name}: {e}")
            return
    else:
        try:
            hero_list = get_all_heroes(hero_randomiser_api_client)
        except Exception as e:
            print(f"Error while attempting to get hero list: {e}")
            return

    if len(hero_list) == 0:
        print("Warning: no applicable heroes found")
        return

    for hero in hero_list:
        try:
            prompt_randomable_state(hero_randomiser_api_client, hero)
        except Exception as e:
            print(f"Error while trying to set randomable status for {hero.name}: {e}")


def prompt_randomable_state(hero_randomiser_api_client: ApiClient, hero: Hero):
    user_input = ""
    while user_input != "y" and user_input != "n":
        user_input = input(f"Make {hero.name} randomable (Y/N)? ").lower()

    if user_input == "y":
        hero.randomable = True
    else:
        hero.randomable = False

    hero_update_response = hero_randomiser_api_client.put(f"/heroes/{hero.id}", hero.json())
    if hero_update_response.status_code != 200:
        error_message = hero_update_response.json()["detail"]
        raise ValueError(error_message)

    print(f"Hero {hero.name} randomable status set to {hero.randomable}")


if __name__ == "__main__":
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        sys.exit(f"Usage: python {sys.argv[0]} <API base URL> [hero name]")
    elif len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        main(sys.argv[1], sys.argv[2])
