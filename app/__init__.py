# Imports
from flask import Flask
from .models import db
from .extensions import ma, limiter, cache
from .blueprints.customer import customers_bp


# Create Flask application instance
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f"config.{config_name}")

    # Init the extension onto the Flask app
    db.init_app(app)  # This adds the db to the app.
    ma.init_app(app)  # This adds Marshmallow to the app.
    limiter.init_app(app)
    cache.init_app(app)
    app.register_blueprint(customers_bp, url_prefix="/customer")

    return app
