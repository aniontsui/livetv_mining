# -*- coding: UTF-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'iVFJyTDbJdMSxB7h4cstgnyopGmDykHwz9XSYYl'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_RECORD_QUERIES = True
    FLASKY_DB_QUERY_TIMEOUT = 10
    DOUYU_MAIN_URL = 'http://www.douyutv.com'
    FLASKY_CHANNELS_PER_PAGE = 20
    FLASKY_ROOMS_PER_PAGE = 20

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///{}'.format(os.path.join(basedir, 'data-dev.sqlite'))


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///{}'.format(os.path.join(basedir, 'data-test.sqlite'))
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///'.format(os.path.join(basedir, 'data.sqlite'))

    @staticmethod
    def init_app(app):
        Config.init_app(app)
        # set production log to file
        from logging import FileHandler, Formatter
        import logging
        filehd = FileHandler('tmp/production.log')
        fileformat = Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        filehd.setFormatter(fileformat)
        filehd.setLevel(logging.INFO)
        app.logger.addHandler(filehd)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
