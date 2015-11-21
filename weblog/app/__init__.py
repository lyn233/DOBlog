__author__ = 'daiguanlin'
# -*- coding:utf-8 -*-
from flask import Flask,render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from weblog.config import Config
from flask_login import LoginManager
from flask_moment import Moment
from flask_migrate import Migrate,MigrateCommand
from flask_pagedown import PageDown
import pymysql

bootstrap = Bootstrap()
db = SQLAlchemy()
pagedown = PageDown()
login_manager = LoginManager()
login_manager.login_view = '.login'
moment = Moment()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(Config)
    Config.init_app(app)
    #config[config_name].init_app(app)
    bootstrap.init_app(app)
    LoginManager(app)
    pagedown.init_app(app)
    moment.init_app(app)
    #db = SQLAlchemy(app)
    #db.create_all()
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return app

