from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()


def setup_extensions(app):
    db.init_app(app)
    Migrate(app, db)


def setup_blueprints(app):
    from blog import blog

    app.register_blueprint(blog, url_prefix="/api/v1")


def create_app(override_settings=None):
    app = Flask(__name__)
    app.config.from_object("settings")
    if override_settings:
        app.config.update(**override_settings)

    setup_extensions(app)
    setup_blueprints(app)

    return app
