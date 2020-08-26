# -*- coding: utf-8 -*-

from app.modules.auth.models import User

from app.modules.auth.utils.jwt import user_identity_lookup, user_loader


def test_user_identity_lookup_should_returns_the_right_field(user):
    u = User.get_by_username(user['username'])
    result = user_identity_lookup(u)
    assert u.id == result


def test_user_loader_should_returns_the_right_user_to_the_passed_identifier(user):
    u = User.get_by_username(user['username'])
    result = user_loader(u.id)
    assert u == result
