from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_apispec import FlaskApiSpec

from . import settings

db = SQLAlchemy()
docs = None


def setup_extensions(app):
    db.init_app(app)
    Migrate(app, db)
    global docs
    docs = FlaskApiSpec(app)


def setup_blueprints(app):
    from .blog import blog, register_docs

    app.register_blueprint(blog, url_prefix="/api/v1")
    register_docs(docs)


def create_app(override_settings=None):
    app = Flask(__name__)
    app.config.from_object(settings)
    if override_settings:
        app.config.update(**override_settings)

    setup_extensions(app)
    setup_blueprints(app)

    return app
