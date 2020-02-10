import databases
import sqlalchemy


import settings


metadata = sqlalchemy.MetaData()
database = None
if settings.TESTING:
    database = databases.Database(settings.TEST_DATABASE_URL, force_rollback=True)
else:
    database = databases.Database(settings.DATABASE_URL)
