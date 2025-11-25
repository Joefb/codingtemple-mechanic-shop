# Imports
from app.models import db, Customer
from .schemas import customer_schema, customers_schema
from app.blueprints.customer import customers_bp
from flask import jsonify, request
from marshmallow import ValidationError


# This will be imported when the app factory pattern is implemented
from app.extensions import limiter, cache


# CUSTOMER ROUTES
# creat customer
@customers_bp.route("", methods=["POST"])
@limiter.limit("2 per day")
def create_customer():
    try:
        data = customer_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_customer = Customer(**data)
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201


# get customer by id
@customers_bp.route("/<int:id>", methods=["GET"])
def get_customer(id):
    customer = db.session.get(Customer, id)
    return customer_schema.jsonify(customer), 200


# get customers list
@customers_bp.route("", methods=["GET"])
def get_users():
    customers = db.session.query(Customer).all()
    return customers_schema.jsonify(customers), 200


# delete customer by id
@customers_bp.route("/<int:id>", methods=["DELETE"])
def delete_customer(id):
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"Error": "Customer not found"}), 404

    db.session.delete(customer)
    db.session.commit()
    return jsonify({"Success": "Customer deleted"}), 200


@customers_bp.route("/<int:id>", methods=["PUT"])
def update_customer(id):
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"Error": "Customer not found"}), 404

    try:
        data = customer_schema.load(request.json, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    for key, value in data.items():
        setattr(customer, key, value)

    db.session.commit()
    return customer_schema.jsonify(customer), 200
