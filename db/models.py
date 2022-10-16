from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


# The fields of this model should remain aligned with the fields in the Hero model
class Heroes(Base):
    __tablename__ = "heroes"

    id = Column(String, primary_key=True, nullable=False, unique=True)
    name = Column(String(length=50), nullable=False)
    randomable = Column(Boolean, default=True, nullable=False)
    hero_type = Column(String(length=50), nullable=False)
