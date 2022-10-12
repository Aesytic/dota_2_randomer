from uuid import uuid4, UUID
import pytest

from api.data_structures import Hero, HeroType, HeroUpdateRequest
from api.hero import create_hero, update_hero
from db import models


@pytest.fixture
def test_hero_row():
    test_hero = Hero(id=UUID("71c7b181-bf67-4a7e-bc61-6c67bc8bb2fc"), name="testing", randomable=True, hero_type=HeroType.MID)

    yield test_hero


def test_create_hero(test_db_session, test_hero_row):
    create_hero(test_db_session, test_hero_row)

    added_hero = test_db_session.query(models.Heroes).first()
    assert added_hero.id == str(test_hero_row.id)
    assert added_hero.name == test_hero_row.name
    assert added_hero.randomable == test_hero_row.randomable
    assert HeroType(added_hero.hero_type) == test_hero_row.hero_type


def test_update_hero_all_fields(test_db_session, test_hero_row):
    create_hero(test_db_session, test_hero_row)
    added_hero = test_db_session.query(models.Heroes).first()
    added_hero_id = added_hero.id

    test_update_request = HeroUpdateRequest(name="new_name", randomable=False, hero_type=HeroType.SUPPORT)

    update_hero(test_db_session, added_hero_id, test_update_request)
    updated_hero = test_db_session.query(models.Heroes).filter(models.Heroes.id == added_hero_id).first()
    assert updated_hero.name == test_update_request.name
    assert updated_hero.randomable == test_update_request.randomable
    assert HeroType(updated_hero.hero_type) == test_update_request.hero_type


def test_update_hero_some_fields(test_db_session, test_hero_row):
    create_hero(test_db_session, test_hero_row)
    added_hero = test_db_session.query(models.Heroes).first()
    added_hero_id = added_hero.id

    test_update_request = HeroUpdateRequest(name=None, randomable=None, hero_type=HeroType.CARRY)

    # Only the hero type field should be updated
    update_hero(test_db_session, added_hero_id, test_update_request)
    updated_hero = test_db_session.query(models.Heroes).filter(models.Heroes.id == added_hero_id).first()
    assert updated_hero.name == added_hero.name
    assert updated_hero.randomable == added_hero.randomable
    assert HeroType(updated_hero.hero_type) == test_update_request.hero_type
