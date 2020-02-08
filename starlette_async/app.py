import sys
import sqlalchemy

from starlette.applications import Starlette
from starlette.config import Config
from starlette.routing import Mount

config = Config(".env")
app = Starlette(debug=config("debug", bool, False))


def setup_routes():
    import blog.views


def create_app():
    sys.path.append(".")
    setup_routes()
