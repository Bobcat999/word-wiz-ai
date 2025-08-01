from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = "sqlite:///./phoneme_db.db"

engine = create_engine(URL_DATABASE, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base = declarative_base()
