import sys

import sqlalchemy
import databases

from starlette.applications import Starlette
from starlette.responses import UJSONResponse
from starlette.exceptions import HTTPException
from starlette.routing import Mount
from spectree import SpecTree

import settings

app = None
database = None
metadata = sqlalchemy.MetaData()
api = SpecTree("starlette")


def setup_routes():
    from blog.views import UserPostListEndpoint

    app.add_route("/api/v1/users/{user_id:int}/posts", UserPostListEndpoint)


async def on_startup():
    await database.connect()


async def on_shutdown():
    await database.disconnect()


async def http_exception(request, exc):
    return UJSONResponse({"errors": [exc.detail]}, status_code=exc.status_code)


def create_app():
    sys.path.append(".")
    global app, database
    if settings.TESTING:
        database = databases.Database(settings.TEST_DATABASE_URL, force_rollback=True)
    else:
        database = databases.Database(settings.DATABASE_URL)

    app = Starlette(
        debug=settings.DEBUG,
        on_startup=[database.connect],
        on_shutdown=[database.disconnect],
        exception_handlers={HTTPException: http_exception},
    )
    setup_routes()
    return app
