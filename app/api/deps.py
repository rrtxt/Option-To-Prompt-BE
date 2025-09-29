from typing import Generator
from sqlmodel import Session
from app.database import engine


def get_session() -> Generator[Session, None, None]:
    """Dependency to get database session"""
    with Session(engine) as session:
        yield session
