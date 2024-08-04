from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings

SQLALCHEMY_DATABASE_URL = settings.database_url


class NotFoundError(Exception):
    pass


class Base(DeclarativeBase):
    pass



engine = create_engine(SQLALCHEMY_DATABASE_URL)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


# Dependency to get the database session
def get_db():
    database = session_local()
    try:
        yield database
    finally:
        database.close()