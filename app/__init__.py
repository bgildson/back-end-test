# -*- coding: utf-8 -*-

import os
import sys

from flask import Flask


CONFIG_NAME_MAPPER = {
    'development': 'config.DevelopmentConfig',
    'testing': 'config.TestingConfig',
    'production': 'config.ProductionConfig',
    'local': 'local_config.LocalConfig',
}


def create_app(flask_env=None, *args, **kwargs) -> Flask:
    """
    Create a Flask application using the app factory pattern
    """

    # create the base app
    app = Flask(__name__, instance_relative_config=True)

    # load correct flask env definition
    if not flask_env:
        env_flask_env = os.getenv('FLASK_ENV')

        if env_flask_env:
            flask_env = env_flask_env
        else:
            msg = 'could not identify which environment the application should use'
            app.logger.error(msg)
            sys.exit(1)

    # load app configurations
    app.config.from_object(CONFIG_NAME_MAPPER[flask_env])

    # initialize modules
    from app import modules

    modules.init_app(app)

    return app
