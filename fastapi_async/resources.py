import databases
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import settings


metadata = MetaData()

database = None
if settings.TESTING:
    database = databases.Database(settings.TEST_DATABASE_URL, force_rollback=True)
else:
    database = databases.Database(settings.DATABASE_URL)

engine = None
if settings.TESTING:
    engine = create_engine(str(settings.TEST_DATABASE_URL))
else:
    engine = create_engine(str(settings.DATABASE_URL))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_session():
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()
