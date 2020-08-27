# -*- coding: utf-8 -*-

from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
import pytest

from app.modules.dids.models import DID


@pytest.fixture(scope='session')
def dids(db: SQLAlchemy):
    """
    Creates some DID's to use in the tests
    """
    dids = []

    for n in range(100):
        did = DID(
            value=f'+55 84 00000-00{n:03}',
            monthy_price=0.03,
            setup_price=3.40,
            currency='USD',
        )
        db.session.add(did)
        dids.append(did)

    db.session.commit()

    return dids


@pytest.fixture(scope='session')
def dids_with_pk_url(app: Flask):
    """
    Creates a factory to create the dids with pk url
    """
    with app.test_request_context():
        return lambda pk: url_for('dids.get_one', pk=pk)


@pytest.fixture(scope='session')
def dids_url(app: Flask):
    """
    Creates a factory to create the dids url
    """
    with app.test_request_context():
        return lambda **kwargs: url_for('dids.get_many', **kwargs)


@pytest.fixture(scope='session')
def did_valid_payload():
    """
    Creates a valid did payload
    """
    return {
        'value': '+55 99 99999-9999',
        'monthyPrice': '0.12',
        'setupPrice': '1.23',
        'currency': 'USD',
    }


@pytest.fixture(scope='session')
def dids_invalid_payloads():
    """
    Creates a list of invalid did payloads
    """
    return [
        'invalid',
        {
            'monthyPrice': '0.12',
            'setupPrice': '1.23',
            'currency': 'USD',
        },
        {
            'value': '+55 11 22222-3333',
            'setupPrice': '1.23',
            'currency': 'USD',
        },
        {
            'value': '+55 11 22222-3333',
            'monthyPrice': '0.12',
            'currency': 'USD',
        },
        {
            'value': '+55 11 22222-3333',
            'monthyPrice': '0.12',
            'setupPrice': '1.23',
        },
        {
            'value': None,
            'monthyPrice': '0.12',
            'setupPrice': '1.23',
            'currency': 'USD',
        },
        {
            'value': '+55 11 22222-3333',
            'monthyPrice': None,
            'setupPrice': '1.23',
            'currency': 'USD',
        },
        {
            'value': '+55 11 22222-3333',
            'monthyPrice': '0.12',
            'setupPrice': None,
            'currency': 'USD',
        },
        {
            'value': '+55 11 22222-3333',
            'monthyPrice': '0.12',
            'setupPrice': '1.23',
            'currency': None,
        },
        {
            'value': '',
            'monthyPrice': '0.12',
            'setupPrice': '1.23',
            'currency': 'USD',
        },
        {
            'value': '+55 11 22222-3333',
            'monthyPrice': '',
            'setupPrice': '1.23',
            'currency': 'USD',
        },
        {
            'value': '+55 11 22222-3333',
            'monthyPrice': '0.12',
            'setupPrice': '',
            'currency': 'USD',
        },
        {
            'value': '+55 11 22222-3333',
            'monthyPrice': '0.12',
            'setupPrice': '1.23',
            'currency': '',
        },
        {
            'value': '+55 11 22222-3333',
            'monthyPrice': 'abc',
            'setupPrice': '1.23',
            'currency': 'USD',
        },
        {
            'value': '+55 11 22222-3333',
            'monthyPrice': '0.12',
            'setupPrice': '1.a23',
            'currency': 'USD',
        },
        {
            'value': '+55 11 22222-3333',
            'monthyPrice': '-0.12',
            'setupPrice': '1.23',
            'currency': 'USD',
        },
        {
            'value': '+55 11 22222-3333',
            'monthyPrice': '0.12',
            'setupPrice': '-1.23',
            'currency': 'USD',
        },
    ]
