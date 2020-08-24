# -*- coding: utf-8 -*-

from flask.app import Flask
import pytest

import app


class TestCreateApp(object):
    def test_factory_should_exists(self):
        assert hasattr(app, 'create_app')

    def test_should_create_a_new_flask_app(self):
        new_app = app.create_app('testing')
        assert isinstance(new_app, Flask)

    def test_should_create_with_empty_flask_env_param(self, monkeypatch):
        monkeypatch.setenv('FLASK_ENV', 'testing')

        new_app = app.create_app()

        assert isinstance(new_app, Flask)

    def test_should_exit_application_when_flask_env_doesnt_exists(self, monkeypatch):
        monkeypatch.delenv('FLASK_ENV', raising=False)

        with pytest.raises(SystemExit) as expected_exception:
            _ = app.create_app()

        assert expected_exception.value.code == 1
