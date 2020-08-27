# -*- coding: utf-8 -*-

import random

from typing import Any, Callable, Dict, List
from unittest import mock
import uuid

from flask import Flask
from flask.testing import FlaskClient

from app.modules.dids.models import DID


class TestGetOne(object):
    def test_should_not_get_one_when_not_authenticated(
        self,
        app: Flask,
        client: FlaskClient,
        dids: List[DID],
        dids_with_pk_url: Callable[[str], str],
    ):
        with app.test_request_context():
            res = client.get(dids_with_pk_url(dids[0].id))
            assert res.status_code == 401

    def test_should_return_an_error_when_the_requested_doesnt_exists(
        self, app: Flask, aclient: FlaskClient, dids_with_pk_url: Callable[[str], str],
    ):
        with app.test_request_context():
            res = aclient.get(dids_with_pk_url(uuid.uuid4()))
            assert res.status_code == 404

    def test_should_handle_an_unexpected_error_properly(
        self,
        app: Flask,
        aclient: FlaskClient,
        dids_with_pk_url: Callable[[Any], str],
        dids: List[DID],
    ):
        with mock.patch.object(
            DID, 'get_by_id', side_effect=Exception('connection error')
        ):
            with app.test_request_context():
                res = aclient.get(dids_with_pk_url(dids[0].id))
                assert res.status_code == 500

    def test_should_return_the_right_did_when_it_exists(
        self,
        app: Flask,
        aclient: FlaskClient,
        dids: List[DID],
        dids_with_pk_url: Callable[[str], str],
    ):
        with app.test_request_context():
            did = random.choice(dids)
            res = aclient.get(dids_with_pk_url(did.id))
            assert res.status_code == 200
            expected = {
                'id': str(did.id),
                'value': did.value,
                'monthyPrice': str(did.monthy_price),
                'setupPrice': str(did.setup_price),
                'currency': did.currency,
            }
            assert res.json == expected


class TestGetMany(object):
    def test_should_not_get_dids_when_not_authenticated(
        self, app: Flask, client: FlaskClient, dids_url: Callable[[Any], str],
    ):
        with app.test_request_context():
            res = client.get(dids_url())
            assert res.status_code == 401

    def test_should_return_an_error_when_start_is_not_a_digit(
        self, app: Flask, aclient: FlaskClient, dids_url: Callable[[Any], str],
    ):
        with app.test_request_context():
            res = aclient.get(dids_url(start='a'))
            assert res.status_code == 400

    def test_should_return_an_error_when_size_is_not_a_digit(
        self, app: Flask, aclient: FlaskClient, dids_url: Callable[[Any], str],
    ):
        with app.test_request_context():
            res = aclient.get(dids_url(size='a'))
            assert res.status_code == 400

    def test_should_return_an_error_when_start_is_less_than_zero(
        self, app: Flask, aclient: FlaskClient, dids_url: Callable[[Any], str],
    ):
        with app.test_request_context():
            res = aclient.get(dids_url(start=-1))
            assert res.status_code == 400

    def test_should_handle_an_unexpected_error_properly(
        self, app: Flask, aclient: FlaskClient, dids_url: Callable[[Any], str],
    ):
        with mock.patch.object(
            DID, 'get_by_start_and_size', side_effect=Exception('connection error')
        ):
            with app.test_request_context():
                res = aclient.get(dids_url())
                assert res.status_code == 500

    def test_should_return_the_maximum_of_twenty_oldest_dids(
        self,
        app: Flask,
        aclient: FlaskClient,
        dids_url: Callable[[Any], str],
        dids: List[DID],
    ):
        with app.test_request_context():
            res = aclient.get(dids_url())
            assert res.status_code == 200
            assert len(res.json) <= 20
            dids_twenty_oldest = dids[:20]
            dids_ids = [d['id'] for d in res.json]
            for did in dids_twenty_oldest:
                assert str(did.id) in dids_ids

    def test_should_return_the_oldest_dids_based_in_the_start(
        self,
        app: Flask,
        aclient: FlaskClient,
        dids: List[DID],
        dids_url: Callable[[Any], str],
    ):
        with app.test_request_context():
            new_start = 42
            res = aclient.get(dids_url(start=new_start))
            assert res.status_code == 200
            assert len(res.json) <= 20
            dids_twenty_oldest = dids[new_start : new_start + 20]
            dids_ids = [d['id'] for d in res.json]
            for did in dids_twenty_oldest:
                assert str(did.id) in dids_ids

    def test_should_return_the_oldest_dids_based_in_the_size(
        self,
        app: Flask,
        aclient: FlaskClient,
        dids: List[DID],
        dids_url: Callable[[Any], str],
    ):
        with app.test_request_context():
            new_size = 42
            res = aclient.get(dids_url(size=new_size))
            assert res.status_code == 200
            assert len(res.json) <= new_size
            dids_twenty_oldest = dids[:new_size]
            dids_ids = [d['id'] for d in res.json]
            for did in dids_twenty_oldest:
                assert str(did.id) in dids_ids

    def test_should_return_the_oldest_dids_based_in_the_start_and_size(
        self,
        app: Flask,
        aclient: FlaskClient,
        dids: List[DID],
        dids_url: Callable[[Any], str],
    ):
        with app.test_request_context():
            new_start = 42
            new_size = 30
            res = aclient.get(dids_url(start=new_start, size=new_size))
            assert res.status_code == 200
            assert len(res.json) <= new_size
            dids_twenty_oldest = dids[new_start : new_start + new_size]
            dids_ids = [d['id'] for d in res.json]
            for did in dids_twenty_oldest:
                assert str(did.id) in dids_ids


class TestCreate(object):
    def test_should_not_create_when_not_authenticated(
        self, app: Flask, client: FlaskClient, dids_url: Callable[[Any], str],
    ):
        with app.test_request_context():
            data = {
                'value': '+55 11 22222-3333',
                'monthyPrice': '0.12',
                'setupPrice': '1.23',
                'currency': 'USD',
            }
            res = client.post(dids_url(), json=data)
            assert res.status_code == 401

    def test_should_return_an_error_when_the_payload_is_invalid(
        self,
        app: Flask,
        aclient: FlaskClient,
        dids_url: Callable[[Any], str],
        dids_invalid_payloads: List[Any],
    ):
        with app.test_request_context():
            for payload in dids_invalid_payloads:
                res = aclient.post(dids_url(), json=payload)
                assert (
                    res.status_code == 400
                ), f'Was expecting 400, but was returned {res.status_code}'

    def test_should_return_an_error_when_creating_with_an_existing_value(
        self, app: Flask, aclient: FlaskClient, dids: List[DID], dids_url: str,
    ):
        with app.test_request_context():
            payload = {
                'value': dids[0].value,
                'monthyPrice': str(dids[0].monthy_price),
                'setupPrice': str(dids[0].setup_price),
                'currency': dids[0].currency,
            }
            res = aclient.post(dids_url(), json=payload)
            assert res.status_code == 409

    def test_should_handle_an_unexpected_error_properly(
        self,
        app: Flask,
        aclient: FlaskClient,
        dids_url: Callable[[Any], str],
        did_valid_payload: Dict[str, any],
    ):
        with mock.patch.object(
            DID, 'get_by_value', side_effect=Exception('connection error')
        ):
            with app.test_request_context():
                res = aclient.post(dids_url(), json=did_valid_payload)
                assert res.status_code == 500

    def test_should_create_successfully_when_the_payload_is_valid(
        self, app: Flask, aclient: FlaskClient, dids_url: Callable[[Any], str],
    ):
        with app.test_request_context():
            payload = {
                'value': '+55 99 99999-9999',
                'monthyPrice': '1.231',
                'setupPrice': '1.239',
                'currency': 'USD',
            }
            res = aclient.post(dids_url(), json=payload)
            assert res.status_code == 201
            did = res.json
            assert 'id' in did
            expected = {
                'id': did['id'],
                'value': payload['value'],
                'monthyPrice': str(int(float(payload['monthyPrice']) * 100) / 100),
                'setupPrice': str(int(float(payload['setupPrice']) * 100) / 100),
                'currency': payload['currency'],
            }
            assert did == expected


class TestUpdate(object):
    def test_should_not_update_when_not_authenticated(
        self,
        app: Flask,
        client: FlaskClient,
        dids: List[DID],
        dids_with_pk_url: Callable[[Any], str],
    ):
        with app.test_request_context():
            did = dids[0]
            payload = {
                'id': did.id,
                'value': '+55 11 22222-3333',
                'monthyPrice': '0.12',
                'setupPrice': '0.12',
                'currency': 'USD',
            }
            res = client.put(dids_with_pk_url(did.id), json=payload)
            assert res.status_code == 401

    def test_should_not_update_an_unexisting_did(
        self,
        app: Flask,
        aclient: FlaskClient,
        dids_with_pk_url: Callable[[Any], str],
        did_valid_payload: Dict[str, Any],
    ):
        with app.test_request_context():
            res = aclient.put(dids_with_pk_url(uuid.uuid4()), json=did_valid_payload)
            assert res.status_code == 404

    def test_should_not_update_when_the_payload_is_invalid(
        self,
        app: Flask,
        aclient: FlaskClient,
        dids_with_pk_url: Callable[[Any], str],
        dids_invalid_payloads: List[Any],
        dids: List[DID],
    ):
        with app.test_request_context():
            for payload in dids_invalid_payloads:
                res = aclient.put(dids_with_pk_url(dids[0].id), json=payload)
                assert (
                    res.status_code == 400
                ), f'Was expecting 400, but was returned {res.status_code}'

    def test_should_not_update_the_value_with_an_existing_value(
        self,
        app: Flask,
        aclient: FlaskClient,
        dids_with_pk_url: Callable[[Any], str],
        dids: List[DID],
    ):
        existing = dids[1]
        payload = {
            'id': str(dids[0].id),
            'value': existing.value,
            'monthyPrice': str(dids[0].monthy_price),
            'setupPrice': str(dids[0].setup_price),
            'currency': dids[0].currency,
        }
        with app.test_request_context():
            res = aclient.put(dids_with_pk_url(dids[0].id), json=payload)
            assert res.status_code == 409

    def test_should_handle_an_unexpected_error_properly(
        self,
        app: Flask,
        aclient: FlaskClient,
        dids_with_pk_url: Callable[[Any], str],
        dids: List[DID],
    ):
        with mock.patch.object(
            DID, 'get_by_id', side_effect=Exception('connection error')
        ):
            with app.test_request_context():
                payload = {
                    'value': '+55 99 99999-9999',
                    'monthyPrice': '1.23',
                    'setupPrice': '1.23',
                    'currency': 'USD',
                }
                res = aclient.put(dids_with_pk_url(dids[0].id), json=payload)
                assert res.status_code == 500

    def test_should_update_every_did_field(
        self,
        app: Flask,
        aclient: FlaskClient,
        dids: List[DID],
        dids_with_pk_url: Callable[[Any], str],
    ):
        with app.test_request_context():
            did = dids[0]
            payload = {
                'id': str(did.id),
                'value': did.value,
                'monthyPrice': str(did.monthy_price),
                'setupPrice': str(did.setup_price),
                'currency': did.currency,
            }
            updates = {
                'value': '+55 88 88888-8888',
                'monthyPrice': f'{float(did.monthy_price) + 1:.2f}',
                'setupPrice': f'{float(did.setup_price) + 1:.2f}',
                'currency': 'EUR',
            }
            for key, value in updates.items():
                payload = {
                    **payload,
                    key: value,
                }
                res = aclient.put(dids_with_pk_url(did.id), json=payload)
                assert (
                    res.status_code == 200
                ), f'Was expecting 200, but was returned {res.status_code}'
                assert (
                    payload == res.json
                ), f'Was expecting {payload}, but was returned {res.json}'


class TestRemove(object):
    def test_should_not_remove_when_not_authenticated(
        self,
        app: Flask,
        client: FlaskClient,
        dids_with_pk_url: Callable[[Any], str],
        dids: List[DID],
    ):
        with app.test_request_context():
            res = client.delete(dids_with_pk_url(dids[0].id))
            assert res.status_code == 401

    def test_should_not_remove_an_unexisting_did(
        self, app: Flask, aclient: FlaskClient, dids_with_pk_url: Callable[[Any], str],
    ):
        with app.test_request_context():
            res = aclient.delete(dids_with_pk_url(uuid.uuid4()))
            assert res.status_code == 404

    def test_should_handle_an_unexpected_error_properly(
        self,
        app: Flask,
        aclient: FlaskClient,
        dids_with_pk_url: Callable[[Any], str],
        dids: List[DID],
    ):
        with mock.patch.object(
            DID, 'get_by_id', side_effect=Exception('connection error')
        ):
            with app.test_request_context():
                res = aclient.delete(dids_with_pk_url(dids[0].id))
                assert res.status_code == 500

    def test_should_remove_an_existing_did(
        self,
        app: Flask,
        aclient: FlaskClient,
        dids_with_pk_url: Callable[[Any], str],
        dids: List[DID],
    ):
        with app.test_request_context():
            res = aclient.delete(dids_with_pk_url(dids[-1].id))
            assert res.status_code == 204
