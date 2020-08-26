# -*- coding: utf-8 -*-

import os


class BaseConfig:
    DEBUG = False
    TESTING = False

    PROJECT_ROOT = os.path.abspath('.')

    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(PROJECT_ROOT, "db.sqlite")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.urandom(32)
    JWT_IDENTITY_CLAIM = 'sub'
    JWT_ERROR_MESSAGE_KEY = 'error'
    JWT_HEADER_TYPE = 'JWT'


class DevelopmentConfig(BaseConfig):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'postgres://postgres:postgres@db:5432/evolux_challenge'

    JWT_SECRET_KEY = 'mysupersecretkey'


class TestingConfig(BaseConfig):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
