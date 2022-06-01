from flask import Flask
from .models import db
from flask_cors import CORS


def create(config_object):
    """
    Build flask app with handlers and blueprints

    :param config_object: Configuration object for flask app
    :return: flask app object
    """
    app = __create(config_object)

    with app.app_context():

        # route: /
        from .auth import auth
        app.register_blueprint(auth)

        # route: /api/applications
        from .api import views
        app.register_blueprint(views.applications)

        from .parser import views
        app.register_blueprint(views.parse)

        db.create_all()
    return app


def __create(config_object):
    """
    Helper to create flask app with database

    :param config_object: Configuration object for flask app
    :return: flask app object
    """
    app = Flask(__name__)
    app.config.from_object(config_object)
    CORS(app, supports_credentials=True)
    db.init_app(app)
    return app

