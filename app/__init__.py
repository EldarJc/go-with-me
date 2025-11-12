from flask import Flask
from flask_login.login_manager import LoginManager
from flask_restx import Api

from .models import db, db_migrate

login_manager = LoginManager()
api = Api()


def create_app(pb_config):

    if not pb_config:
        raise ValueError("Missing configuration!")

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(pb_config)

    db.init_app(app=app)
    db_migrate.init_app(app=app)
    login_manager.init_app(app=app)
    api.init_app(app)

    return app
