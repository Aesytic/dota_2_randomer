import sys
import os
from pathlib import Path
import pytest
from alembic.command import upgrade
from alembic.config import Config

sys.path.append(os.path.join(os.getcwd(), "db"))

from db.sqlite import engine_factory, sessionmaker_factory


@pytest.fixture
def test_db_session():
    db_directory = os.path.join(os.getcwd(), "db")
    alembic_config_ini_path = os.path.join(db_directory, "alembic.ini")
    alembic_directory = os.path.join(db_directory, "alembic")

    test_sqlite_db_file = os.path.join(Path(os.getcwd()) / "test/test_db.sqlite3")
    test_sqlite_db_url = f"sqlite:///{test_sqlite_db_file}"

    alembic_config = Config(alembic_config_ini_path)
    alembic_config.set_main_option("script_location", alembic_directory)
    alembic_config.set_main_option("sqlalchemy.url", test_sqlite_db_url)
    upgrade(alembic_config, "head")

    engine = engine_factory(test_sqlite_db_url)
    sessionmaker = sessionmaker_factory(engine)
    session = sessionmaker()

    yield session

    session.close()
    os.remove(test_sqlite_db_file)
