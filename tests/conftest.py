# -*- coding: utf-8 -*-

import pytest

from app import create_app


@pytest.fixture(scope='session')
def app():
    """
    Creates an app injectable in session level
    """
    return create_app('testing')


@pytest.fixture(scope='session')
def client(app):
    """
    Creates a http client injectable in session level
    """
    return app.test_client()
