# Imports
from flask import Flask
from .models import db
from .extensions import ma, limiter, cache
from .blueprints.customer import customers_bp
from .blueprints.tech import techs_bp
from .blueprints.invoice import invoices_bp


# Create Flask application instance
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f"config.{config_name}")

    # Init the extension onto the Flask app
    db.init_app(app)  # This adds the db to the app.
    ma.init_app(app)  # This adds Marshmallow to the app.
    limiter.init_app(app)
    cache.init_app(app)
    # Create prefixed blueprint routes
    app.register_blueprint(customers_bp, url_prefix="/customer")
    app.register_blueprint(techs_bp, url_prefix="/tech")
    app.register_blueprint(invoices_bp, url_prefix="/invoice")

    with app.app_context():
        from app.models import Tech
        from werkzeug.security import generate_password_hash

        # Create a admin user if not exists.
        # Change password!!!
        if not db.session.query(Tech).filter_by(last_name="admin").first():
            admin_tech = Tech(
                first_name="admin",
                last_name="admin",
                position="admin",
                phone="000-000-0000",
                password=generate_password_hash("password"),
            )
            db.session.add(admin_tech)
            db.session.commit()

    return app
