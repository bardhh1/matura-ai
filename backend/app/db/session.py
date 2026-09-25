from dataclasses import dataclass

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker


@dataclass(frozen=True)
class Database:
    engine: Engine
    session_factory: sessionmaker[Session]


def create_database(database_url: str) -> Database:
    connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
    engine = create_engine(
        database_url,
        pool_pre_ping=True,
        connect_args=connect_args,
    )
    return Database(
        engine=engine,
        session_factory=sessionmaker(
            bind=engine,
            autoflush=False,
            expire_on_commit=False,
        ),
    )
