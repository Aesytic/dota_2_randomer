from pathlib import Path
import os
import os.path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLITE_FILE_PATH = os.path.join(Path(os.getcwd()) / "db" / "db.sqlite3")
SQLITE_URL = f"sqlite:///{SQLITE_FILE_PATH}"

engine = create_engine(
    SQLITE_URL, connect_args={"check_same_thread": False}
)

SqliteSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
