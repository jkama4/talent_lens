import os

from .models import Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL: str = os.getenv(
    "DATABASE_URL"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def setup_database() -> None:
    Base.metadata.create_all(bind=engine)
