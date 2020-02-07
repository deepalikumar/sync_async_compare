import sys

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_apispec import FlaskApiSpec


db = SQLAlchemy()
docs = None


def setup_extensions(app):
    db.init_app(app)
    Migrate(app, db)
    global docs
    docs = FlaskApiSpec(app)


def setup_blueprints(app):
    import blog.views

    app.register_blueprint(blog.views.blueprint, url_prefix="/api/v1")
    blog.views.register_docs(docs)


def setup_error_handlers(app):
    app.register_error_handler(400, _handle_bad_request)
    app.register_error_handler(422, _handle_bad_request)
    app.register_error_handler(500, _handle_exception)


def setup_commands(app):
    from .commands import data_cli

    app.cli.add_command(data_cli)


def _handle_bad_request(err):
    headers = err.data.get("headers", None)
    messages = err.data.get("messages", ["Invalid request."])
    if headers:
        return jsonify({"errors": messages}), err.code, headers
    else:
        return jsonify({"errors": messages}), err.code


def _handle_exception(exception):
    return jsonify({"errors": "Server error"}), 500


def create_app(override_settings=None):
    app = Flask(__name__)
    sys.path.append(".")
    app.config.from_object("settings")
    if override_settings:
        app.config.update(**override_settings)

    setup_extensions(app)
    setup_blueprints(app)
    setup_commands(app)
    setup_error_handlers(app)

    return app
