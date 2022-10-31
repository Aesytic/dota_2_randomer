from uuid import uuid4, UUID
import pytest
import random

from api.data_structures import Hero, HeroType, HeroUpdateRequest
from api.hero import read_all_heroes, create_hero, read_hero, update_hero, delete_hero, get_random_hero
from db import models


@pytest.fixture
def test_hero_row(test_db_session):
    test_hero = models.Heroes(id="71c7b181-bf67-4a7e-bc61-6c67bc8bb2fc",
                              name="testing",
                              randomable=True,
                              hero_type=HeroType.MID.value)
    test_db_session.add(test_hero)
    test_db_session.commit()

    yield test_hero


@pytest.mark.parametrize("filters,expected_num_entries",
                         [((None, None, None, None), 2),
                          (("71c7b181-bf67-4a7e-bc61-6c67bc8bb2fc", None, None, None), 1),
                          ((None, "testing_2", None, None), 1),
                          ((None, None, True, None), 1),
                          ((None, None, None, HeroType.CARRY.value), 1),
                          (("broken filter", None, None, None), 0)])
def test_read_all_heroes(test_db_session, filters, expected_num_entries):
    test_row_1 = Hero(id=UUID("71c7b181-bf67-4a7e-bc61-6c67bc8bb2fc"),
                      name="testing",
                      randomable=True,
                      hero_type=HeroType.MID)
    test_row_2 = Hero(id=UUID("44322a6a-b2ef-4807-acc8-a32fdd7125ab"),
                      name="testing_2",
                      randomable=False,
                      hero_type=HeroType.CARRY)
    test_rows = [models.Heroes(**test_row_1.to_dict()), models.Heroes(**test_row_2.to_dict())]
    test_db_session.add_all(test_rows)
    test_db_session.commit()

    all_heroes = read_all_heroes(test_db_session, *filters)
    all_heroes_dict = {hero_row.id: hero_row for hero_row in all_heroes}

    assert len(all_heroes_dict) == expected_num_entries


def test_create_hero(test_db_session):
    test_hero = Hero(id=UUID("6e4393ef-9ae8-4a1c-b8bc-86da28c4aae9"),
                     name="test_new_hero",
                     randomable=True,
                     hero_type=HeroType.SUPPORT.value)

    create_hero(test_db_session, test_hero)

    added_hero = test_db_session.query(models.Heroes).first()

    assert added_hero.id == str(test_hero.id)
    assert added_hero.name == test_hero.name
    assert added_hero.randomable == test_hero.randomable
    assert HeroType(added_hero.hero_type) == test_hero.hero_type


def test_read_hero_valid(test_db_session, test_hero_row):
    queried_hero = read_hero(test_db_session, test_hero_row.id)

    assert test_hero_row.id == str(queried_hero.id)
    assert test_hero_row.name == queried_hero.name
    assert test_hero_row.randomable == queried_hero.randomable
    assert test_hero_row.hero_type == queried_hero.hero_type.value


def test_read_hero_invalid(test_db_session):
    test_hero_id = "fake_hero"
    with pytest.raises(ValueError) as e:
        read_hero(test_db_session, test_hero_id)

    assert str(e.value) == f"Hero {test_hero_id} not found"


@pytest.mark.parametrize("test_update_request",
                         [
                             # Update all fields
                             (HeroUpdateRequest(name="new_name", randomable=False, hero_type=HeroType.SUPPORT)),
                             # Update some fields
                             (HeroUpdateRequest(name=None, randomable=None, hero_type=HeroType.CARRY))
                         ])
def test_update_hero_valid(test_db_session, test_hero_row, test_update_request):
    update_hero(test_db_session, test_hero_row.id, test_update_request)
    updated_hero = test_db_session.query(models.Heroes).filter(models.Heroes.id == str(test_hero_row.id)).first()

    assert updated_hero.name == test_update_request.name or test_hero_row.name
    assert updated_hero.randomable == test_update_request.randomable or test_hero_row.randomable
    assert HeroType(updated_hero.hero_type) == test_update_request.hero_type or test_hero_row.hero_type


def test_update_hero_invalid(test_db_session):
    with pytest.raises(ValueError) as e:
        fake_uuid = uuid4()
        update_hero(test_db_session, fake_uuid, HeroUpdateRequest())

    assert str(e.value) == f"Hero ID {fake_uuid} not found"


def test_delete_hero_valid(test_db_session, test_hero_row):
    delete_hero(test_db_session, test_hero_row.id)
    queried_deleted_hero = test_db_session.query(models.Heroes).\
        filter(models.Heroes.id == str(test_hero_row.id)).first()

    assert queried_deleted_hero is None


def test_delete_hero_invalid(test_db_session):
    with pytest.raises(ValueError) as e:
        fake_uuid = uuid4()
        delete_hero(test_db_session, fake_uuid)

    assert str(e.value) == f"Hero ID {fake_uuid} not found"


def test_get_random_hero_valid(test_db_session):
    test_row_1 = Hero(id=UUID("71c7b181-bf67-4a7e-bc61-6c67bc8bb2fc"),
                      name="testing",
                      randomable=True,
                      hero_type=HeroType.MID)
    test_row_2 = Hero(id=UUID("44322a6a-b2ef-4807-acc8-a32fdd7125ab"),
                      name="testing_2",
                      randomable=True,
                      hero_type=HeroType.CARRY)
    test_row_3 = Hero(id=UUID("4cd2ac09-cb8d-4409-8287-f452e455bce9"),
                      name="testing_3",
                      randomable=True,
                      hero_type=HeroType.SUPPORT)
    test_rows = [models.Heroes(**test_row_1.to_dict()),
                 models.Heroes(**test_row_2.to_dict()),
                 models.Heroes(**test_row_3.to_dict())]
    test_db_session.add_all(test_rows)
    test_db_session.commit()

    # This seed should output the following order of rows in this test:
    #   row 1, row 2, row 2, row 2, row 1, row 3
    random.seed(a=5000)

    random_1 = get_random_hero(test_db_session)
    random_2 = get_random_hero(test_db_session)
    random_3 = get_random_hero(test_db_session)
    random_4 = get_random_hero(test_db_session)
    random_5 = get_random_hero(test_db_session)
    random_6 = get_random_hero(test_db_session)

    assert random_1.id == test_row_1.id
    assert random_2.id == test_row_2.id
    assert random_3.id == test_row_2.id
    assert random_4.id == test_row_2.id
    assert random_5.id == test_row_1.id
    assert random_6.id == test_row_3.id


def test_get_random_hero_invalid(test_db_session):
    # No randomable heroes in DB
    test_row_1 = Hero(id=UUID("71c7b181-bf67-4a7e-bc61-6c67bc8bb2fc"),
                      name="testing",
                      randomable=False,
                      hero_type=HeroType.MID)
    test_row_2 = Hero(id=UUID("44322a6a-b2ef-4807-acc8-a32fdd7125ab"),
                      name="testing_2",
                      randomable=False,
                      hero_type=HeroType.CARRY)
    test_row_3 = Hero(id=UUID("4cd2ac09-cb8d-4409-8287-f452e455bce9"),
                      name="testing_3",
                      randomable=False,
                      hero_type=HeroType.SUPPORT)
    test_rows = [models.Heroes(**test_row_1.to_dict()),
                 models.Heroes(**test_row_2.to_dict()),
                 models.Heroes(**test_row_3.to_dict())]
    test_db_session.add_all(test_rows)
    test_db_session.commit()

    with pytest.raises(ValueError) as e:
        get_random_hero(test_db_session)

    assert str(e.value) == "No randomable heroes in DB"
