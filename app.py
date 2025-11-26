from app.models import db
from app import create_app

apps = create_app("DevelopmentConfig")
with apps.app_context():
    # db.drop_all()
    db.create_all()

apps.run()

# from flask import Flask, jsonify, request
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
# from sqlalchemy import String, Float, ForeignKey, Table, Column, Date
# from datetime import date
# from flask_marshmallow import Marshmallow  # Importing Marshmallow class
# from marshmallow import ValidationError
#
# # Limiter imports
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address
#
# # Flask cache imports (if needed in future)
# from flask_caching import Cache
#
# # This will be imported when the app factory pattern is implemented
# from app.extensions import limiter


# Connect to database
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"


# # Create Marshmallow instance
# ma = Marshmallow()

# # Create Limiter instance
# limiter = Limiter(get_remote_address, default_limits=["200 per day", "50 per hour"])
#
# # Create Cache instance (if needed in future)
# cache = Cache()
#
# # # Init the extension onto the Flask app
# # db.init_app(app)  # This adds the db to the app.
# # ma.init_app(app)  # This adds Marshmallow to the app.
# limiter.init_app(app)
# cache.init_app(app)
#
#
# class InvoiceSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Invoice
#
#
# class TechSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Tech
#
#
# # Create instances of the schemas
# invoice_schema = InvoiceSchema()
# invoices_schema = InvoiceSchema(many=True)
# tech_schema = TechSchema()
# techs_schema = TechSchema(many=True)
#
#
# ### ROUTES ###
#
#
#
#
# ## TEC ROUTES ##
# # create tech
# @app.route("/tech", methods=["POST"])
# def create_tech():
#     try:
#         data = tech_schema.load(request.json)
#     except ValidationError as err:
#         return jsonify(err.messages), 400
#
#     new_tech = Tech(**data)
#     db.session.add(new_tech)
#     db.session.commit()
#     return tech_schema.jsonify(new_tech), 201
#
#
# # get tech by id
# @app.route("/tech/<int:id>", methods=["GET"])
# def get_tech(id):
#     tech = db.session.get(Tech, id)
#     return tech_schema.jsonify(tech), 200
#
#
# # get techs list
# @app.route("/tech", methods=["GET"])
# def get_techs():
#     techs = db.session.query(Tech).all()
#     return jsonify(techs_schema.dump(techs, many=True)), 200
#
#
# # delete tech by id
# @app.route("/tech/<int:id>", methods=["DELETE"])
# def delete_tech(id):
#     tech = db.session.get(Tech, id)
#     if not tech:
#         return jsonify({"Error": "Tech not found"}), 404
#
#     db.session.delete(tech)
#     db.session.commit()
#     return jsonify({"Success": "Tech deleted"}), 200
#
#
# ## INVOICE ROUTES ##
# @app.route("/invoice", methods=["POST"])
# def create_invoice():
#     try:
#         data = invoice_schema.load(request.json)
#     except ValidationError as err:
#         return jsonify(err.messages), 400
#
#     new_invoice = Invoice(**data)
#     db.session.add(new_invoice)
#     db.session.commit()
#     return invoice_schema.jsonify(new_invoice), 201
#
#
# # get invoice by id
# @app.route("/invoice/<int:id>", methods=["GET"])
# def get_invoice(id):
#     invoice = db.session.get(Invoice, id)
#     return jsonify(invoice_schema.dump(invoice)), 200
#
#
# # get invoices
# @app.route("/invoice", methods=["GET"])
# def get_invoices():
#     invoices = db.session.query(Invoice).all()
#     return jsonify(invoices_schema.dump(invoices)), 200
#
#
# # delete invoices by id
# @app.route("/invoice/<int:id>", methods=["DELETE"])
# def delete_invoice(id):
#     invoice = db.session.get(Invoice, id)
#     if not invoice:
#         return jsonify({"Error": "Invoice not found"}), 400
#
#     db.session.delete(invoice)
#     db.session.commit()
#     return jsonify({"Success": "Invoice Deleted"}), 200
#
#
# with app.app_context():
#     db.create_all()  # Create the database and the database table(s)
#
# # Run the app
# if __name__ == "__main__":
#     app.run(debug=True)
