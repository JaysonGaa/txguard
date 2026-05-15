import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, declarative_base

engine = sa.create_engine(
    "sqlite:///txguard.db",
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

