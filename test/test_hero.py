from uuid import uuid4, UUID
import pytest

from api.data_structures import Hero, HeroType, HeroUpdateRequest
from api.hero import create_hero, read_hero, update_hero
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


def test_read_hero_valid(test_db_session, test_hero_row):
    added_hero = create_hero(test_db_session, test_hero_row)
    added_hero_id = added_hero.id

    queried_hero = read_hero(test_db_session, added_hero_id)

    assert added_hero.id == queried_hero.id
    assert added_hero.name == queried_hero.name
    assert added_hero.randomable == queried_hero.randomable
    assert added_hero.hero_type == queried_hero.hero_type


def test_read_hero_invalid(test_db_session):
    with pytest.raises(ValueError) as e:
        fake_uuid = uuid4()
        read_hero(test_db_session, fake_uuid)

    assert str(e.value) == f"Hero ID {fake_uuid} not found"


@pytest.mark.parametrize("test_update_request",
                         [
                             # Update all fields
                             (HeroUpdateRequest(name="new_name", randomable=False, hero_type=HeroType.SUPPORT)),
                             # Update some fields
                             (HeroUpdateRequest(name=None, randomable=None, hero_type=HeroType.CARRY))
                         ])
def test_update_hero_valid(test_db_session, test_hero_row, test_update_request):
    create_hero(test_db_session, test_hero_row)
    added_hero = test_db_session.query(models.Heroes).first()
    added_hero_id = added_hero.id

    update_hero(test_db_session, added_hero_id, test_update_request)
    updated_hero = test_db_session.query(models.Heroes).filter(models.Heroes.id == added_hero_id).first()

    assert updated_hero.name == test_update_request.name or added_hero.name
    assert updated_hero.randomable == test_update_request.randomable or added_hero.randomable
    assert HeroType(updated_hero.hero_type) == test_update_request.hero_type or added_hero.hero_type


def test_update_hero_invalid(test_db_session):
    with pytest.raises(ValueError) as e:
        fake_uuid = uuid4()
        update_hero(test_db_session, fake_uuid, HeroUpdateRequest())

    assert str(e.value) == f"Hero ID {fake_uuid} not found"
