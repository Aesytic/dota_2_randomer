from uuid import uuid4

from api.data_structures import Hero, HeroType
from api.hero import create_hero


TEST_HERO = Hero(id=uuid4(), name="testing", randomable=True, hero_type=HeroType.MID)


def test_create_hero(mock_session_fixture):
    create_hero(mock_session_fixture, TEST_HERO)

    added_hero = mock_session_fixture.add_buffer[0]
    assert added_hero.id == str(TEST_HERO.id)
    assert added_hero.name == TEST_HERO.name
    assert added_hero.randomable == TEST_HERO.randomable
    assert HeroType(added_hero.hero_type) == TEST_HERO.hero_type
