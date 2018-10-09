#encoding: utf-8

import os


class Config:
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    FLASKY_POSTS_PER_PAGE = 20

    DIALECT = 'mysql'
    DRIVER = 'mysqldb'
    USERNAME = 'root'
    PASSWORD = 'root'
    HOST = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'flask_demo'
    SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST,
                                                                           PORT, DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # CSRF保护
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or '*\xff\x93\xc8w\x13\x0e@3\xd6\x82\x0f\x84\x18\xe7\xd9\\|\x04e\xb9(\xfd\xc3'


    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True

    # email config
    MAIL_SERVER = 'smtp.sina.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'test_send_mail_2@sina.com'
    MAIL_PASSWORD = 'testtest'
    MAIL_DEBUG = True
    FLASKY_MAIL_SENDER = os.environ.get('MAIL_USERNAME') or MAIL_USERNAME
    FLASKY_MAIL_SUBJECT_PREFIX = '[Vulab]'



class TestingConfig(Config):
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
