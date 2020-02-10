import sys

import sqlalchemy
import databases

from starlette.applications import Starlette
from starlette.responses import UJSONResponse
from starlette.exceptions import HTTPException
from starlette.routing import Mount, Route

import settings

app = None
database = None
metadata = sqlalchemy.MetaData()


def setup_routes():
    from blog.views import UserPostListEndpoint

    routes = [
        Mount(
            "/api/v1",
            name="v1",
            routes=[
                Route(
                    "/users/{user_id:int}/posts", UserPostListEndpoint, name="user_list"
                )
            ],
        )
    ]
    return routes


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
        routes=setup_routes(),
        on_startup=[database.connect],
        on_shutdown=[database.disconnect],
        exception_handlers={HTTPException: http_exception,},
    )
    return app
