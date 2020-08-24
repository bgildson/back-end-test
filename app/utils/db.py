# -*- coding: utf-8 -*-
"""
Stores the central db instance
"""

from flask_sqlalchemy import SQLAlchemy


db: SQLAlchemy = SQLAlchemy()
