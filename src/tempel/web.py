from flask import Flask
import os
import sys

from flask_swagger_ui import get_swaggerui_blueprint

from tempel.adapters import orm
from tempel.conf import Settings
from tempel.controllers import user_controllers_bp
from tempel.services import query

sys.path.append(os.environ["PYTHONPATH"])


def create_app(settings: Settings):
    """Create the Flask WSGI application instance.

    Returns:
        A Flask WSGI application instance.
    
    """

    app = Flask(__name__)

    app.secret_key = os.environ["SECRET_KEY"]

    # orm.start_mappers() # Already in SessionFactory
    if settings.database_url.startswith("postgres://"):
        settings.database_url = settings.database_url.replace("postgres://", "postgresql://", 1)
    session_factory = orm.SessionFactory(settings)
    app.query_engine = query.SqlAlchemyQueryEngine(session_factory)

    swaggerui_blueprint = get_swaggerui_blueprint(
        base_url="/docs",
        api_url="/static/openapi.yml",
        config={
            "app_name": "Test application"
        },
    )

    app.register_blueprint(swaggerui_blueprint)
    app.register_blueprint(user_controllers_bp)

    return app