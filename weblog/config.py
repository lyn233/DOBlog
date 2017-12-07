__author__ = 'll'
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'guess'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:8511@localhost/blog'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):

    DEBUG = True


class ProductionConfig(Config):

    pass


config = {'development': DevelopmentConfig, 'default': DevelopmentConfig, 'production': ProductionConfig}
