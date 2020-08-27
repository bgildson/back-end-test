# -*- coding: utf-8 -*-

from __future__ import annotations
from datetime import datetime
from typing import List
import uuid

from sqlalchemy_utils import types

from app.utils.db import db


class DID(db.Model):
    """
    Represents an app did
    """

    __tablename__ = 'dids'

    id = db.Column(types.UUIDType(), primary_key=True, default=uuid.uuid4)
    value = db.Column(db.String(20), unique=True, nullable=False)
    monthy_price = db.Column(db.Numeric(precision=15, scale=2), nullable=False)
    setup_price = db.Column(db.Numeric(precision=15, scale=2), nullable=False)
    currency = db.Column(db.String(3))
    created_at = db.Column(db.DateTime, default=datetime.now)

    @classmethod
    def get_by_id(cls, pk) -> DID:
        return DID.query.filter_by(id=pk).first()

    @classmethod
    def get_by_start_and_size(cls, start: int, size: int) -> List[DID]:
        return DID.query.order_by('created_at').offset(start).limit(size).all()

    @classmethod
    def get_by_value(cls, value: str) -> DID:
        return DID.query.filter_by(value=value).first()
