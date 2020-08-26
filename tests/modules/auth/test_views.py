# -*- coding: utf-8 -*-

from flask import Flask
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
from typing import Dict, Any
from unittest import mock

from app.modules.auth.models import User


class TestRegister(object):
    def test_should_return_an_error_when_payload_is_invalid(
        self,
        app: Flask,
        client: FlaskClient,
        user: Dict[str, Any],
        auth_register_url: str,
    ):
        with app.test_request_context():
            payloads = (
                'invalid',
                {'username': user['username']},
                {'password': '112233'},
            )
            for payload in payloads:
                res = client.post(auth_register_url, json=payload)
                assert res.status_code == 400

    def test_should_return_an_error_when_the_username_already_exists(
        self,
        app: Flask,
        client: FlaskClient,
        user: Dict[str, Any],
        auth_register_url: str,
    ):
        with app.test_request_context():
            payload = {'username': user['username'], 'password': 'abcdef'}
            res = client.post(auth_register_url, json=payload)
            assert res.status_code == 409

    def test_should_handle_an_unexpected_error_properly(
        self,
        app: Flask,
        db: SQLAlchemy,
        client: FlaskClient,
        user: Dict[str, Any],
        auth_register_url: str,
    ):
        # simulate a database connection error
        with mock.patch.object(
            db.session, 'commit', side_effect=Exception('connection error')
        ):
            with app.test_request_context():
                payload = {
                    'username': f'{user["username"]}new',
                    'password': user['password'],
                }
                res = client.post(auth_register_url, json=payload)
                assert res.status_code == 500

    def test_should_return_the_access_token_when_register_successfully(
        self,
        app: Flask,
        client: FlaskClient,
        user: Dict[str, Any],
        auth_register_url: str,
    ):
        with app.test_request_context():
            payload = {'username': f'{user["username"]}new', 'password': '654321'}
            res = client.post(auth_register_url, json=payload)
            assert res.status_code == 200
            assert 'access_token' in res.get_json()


class TestLogin(object):
    def test_should_return_errors_when_payload_is_invalid(
        self,
        app: Flask,
        client: FlaskClient,
        user: Dict[str, Any],
        auth_login_url: str,
    ):
        with app.test_request_context():
            payloads = (
                'invalid',
                {'username': user['username']},
                {'password': user['password']},
            )
            for payload in payloads:
                res = client.post(auth_login_url, json=payload)
                assert res.status_code == 400

    def test_should_return_an_error_when_credentials_doesnt_matches(
        self,
        app: Flask,
        client: FlaskClient,
        user: Dict[str, Any],
        auth_login_url: str,
    ):
        with app.test_request_context():
            payloads = (
                {'username': user['username'], 'password': f'{user["password"]}0'},
                {
                    'username': f'{user["username"]}unexisting',
                    'password': user['password'],
                },
            )
            for payload in payloads:
                res = client.post(auth_login_url, json=payload)
                assert res.status_code == 401

    def test_should_return_an_error_when_occur_an_unexpected_exception(
        self,
        app: Flask,
        client: FlaskClient,
        user: Dict[str, Any],
        auth_login_url: str,
    ):
        # simulate a database connection error
        with mock.patch.object(
            User,
            'get_by_username_and_password',
            side_effect=Exception('connection error'),
        ):
            with app.test_request_context():
                payload = {'username': user['username'], 'password': user['password']}
                res = client.post(auth_login_url, json=payload)
                assert res.status_code == 500

    def test_should_return_token_with_correct_username_and_password(
        self,
        app: Flask,
        client: FlaskClient,
        user: Dict[str, Any],
        auth_login_url: str,
    ):
        with app.test_request_context():
            payload = {'username': user['username'], 'password': user['password']}
            res = client.post(auth_login_url, json=payload)
            assert res.status_code == 200
            assert 'access_token' in res.json
