from pathlib import Path
import os
import os.path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLITE_FILE_PATH = os.path.join(Path(os.getcwd()) / "db" / "db.sqlite3")
SQLITE_URL = f"sqlite:///{SQLITE_FILE_PATH}"


def engine_factory(db_url=SQLITE_URL):
    engine = create_engine(
        db_url, connect_args={"check_same_thread": False}
    )

    return engine


def sessionmaker_factory(engine):
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    return session
