# -*- coding: utf-8 -*-

import os


class BaseConfig:
    DEBUG = False
    TESTING = False

    PROJECT_ROOT = os.path.abspath('.')

    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_DATABASE_URI = \
        'sqlite:///%s' % (os.path.join(PROJECT_ROOT, 'db.sqlite'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'postgres://postgres:postgres@db:5432/evolux_challenge'


class TestingConfig(BaseConfig):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class ProductionConfig(BaseConfig):
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
