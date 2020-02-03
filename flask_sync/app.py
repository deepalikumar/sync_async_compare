from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()


def setup_extensions(app):
    db.init_app(app)
    Migrate(app, db)


def create_app(override_settings=None):
    app = Flask(__name__)
    app.config.from_object("settings")
    if override_settings:
        app.config.update(**override_settings)

    setup_extensions(app)

    return app
