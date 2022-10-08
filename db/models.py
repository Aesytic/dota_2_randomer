from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Heroes(Base):
    __tablename__ = "heroes"

    id = Column(String, primary_key=True, nullable=False)
    name = Column(String(length=50), nullable=False)
    randomable = Column(Boolean, default=True, nullable=False)
    hero_type = Column(String(length=50), nullable=False)
