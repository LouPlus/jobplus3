#coding=utf-8


import datetime
from flask import Flask
from jobplus.config import configs, CURRENT_ENV
from jobplus.models import db, User
from flask_migrate import Migrate
from flask_login import LoginManager


# 注册模板过滤器
def register_filters(app):

    @app.template_filter()
    def timesince(value):
        """
        格式化时间
        """
        now = datetime.datetime.utcnow()
        delta = now - value
        if delta.days > 365:
            return '{}年前'.format(delta.days // 365)
        if delta.days > 30:
            return '{}月前'.format(delta.days // 30)
        if delta.days > 0:
            return '{}天前'.format(delta.days)
        if delta.seconds > 3600:
            return '{}小时前'.format(delta.seconds // 3600)
        if delta.seconds > 60:
            return '{}分钟前'.format(delta.seconds // 60)
        return '刚刚'

def register_extensions(app):
    """
    添加扩展
    """
    db.init_app(app)
    Migrate(app, db)

    login_manager = LoginManager()
    # 设置安全级别 None、'basic'、'strong'
    # flask_login 会记住客户端的IP地址和用户代理信息
    login_manager.session_protection="strong"

    login_manager.init_app(app)

    # 这是回调函数
    # 登录验证时LoginManger从数据库加载用户
    @login_manager.user_loader
    def user_loader(id):
        return User.query.get(id)
    # 指定登录视图
    login_manager.login_view = 'front.login'


def register_blueprints(app):
    """
    蓝图注册
    """
    from .handlers import front, user, company, admin, job
    app.register_blueprint(front)
    app.register_blueprint(user)
    app.register_blueprint(company)
    app.register_blueprint(job)
    app.register_blueprint(admin)


def create_app():
    """
    可以根据传入的 config 名称，加载不同的配置
    """
    app = Flask(__name__)
    app.config.from_object(configs.get(CURRENT_ENV))

    register_extensions(app)
    register_blueprints(app)
    register_filters(app)
    return app