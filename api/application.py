from flask import Flask, g

from api.config import DefaultConfig
from flaskext.principal import Principal, identity_loaded
from api.extensions import db
from api.rpc import rpc
from api.models import User


DEFAULT_APP_NAME = "api"


def create_app(config=None, app_name=None, modules=None):

    if app_name is None:
        app_name = DEFAULT_APP_NAME

    app = Flask(app_name)
    configure_app(app, config)
    configure_extensions(app)
    configure_blueprints(app)
    configure_identity(app)
    return app


def configure_app(app, config):
    app.config.from_object(config or DefaultConfig())
    app.config.from_envvar('APP_CONFIG', silent=True)


def configure_extensions(app):
    db.init_app(app)


def configure_blueprints(app):
    app.register_blueprint(rpc, url_prefix='/rpc')


def configure_identity(app):
    Principal(app)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        g.user = User.query.from_identity(identity)

    assert on_identity_loaded
