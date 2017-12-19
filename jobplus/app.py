#coding=utf-8

from flask import Flask
from jobplus.config import configs, CURRENT_ENV
from jobplus.models import db
from flask_migrate import Migrate


def register_extensions(app):
    pass


def register_blueprints(app):
    from .handlers import front
    app.register_blueprint(front)


def create_app():
    """可以根据传入的 config 名称，加载不同的配置
    """
    app = Flask(__name__)
    app.config.from_object(configs.get(CURRENT_ENV))
    db.init_app(app)
    Migrate(app, db)
    register_extensions(app)
    register_blueprints(app)
    return app