# Imports
from app.models import db, Customer
from .schemas import (
    customer_schema,
    customers_schema,
    create_customer_schema,
    login_schema,
)
from app.blueprints.customer import customers_bp
from flask import jsonify, request
from marshmallow import ValidationError
from app.extensions import limiter
from werkzeug.security import check_password_hash, generate_password_hash
from app.util.auth import (
    admin_or_tech_token_required,
    encode_token,
    token_required,
    admin_token_required,
)


# CUSTOMER ROUTES
# customer login
@customers_bp.route("/login", methods=["POST"])
@limiter.limit("5 per 10 minute")
def login():
    try:
        # get my user credentials - responsibility for my client
        data = login_schema.load(request.json)  # JSON -> Python
    except ValidationError as e:
        return jsonify(e.messages), 400

    user = db.session.query(Customer).where(Customer.email == data["email"]).first()

    if user and check_password_hash(user.password, data["password"]):
        # Create token for user
        token = encode_token(user.id)
        return jsonify(
            {
                "message": f"Welcome {user.first_name}",
                "token": token,
            }
        ), 200


# create customer
@customers_bp.route("", methods=["POST"])
@limiter.limit("5 per day")
@admin_token_required
def create_customer():
    try:
        data = create_customer_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    data["password"] = generate_password_hash(
        data["password"]
    )  # resetting the password key's value, to the hash of the current value
    new_customer = Customer(**data)
    db.session.add(new_customer)
    db.session.commit()
    return create_customer_schema.jsonify(new_customer), 201


# get current logged in customer
@customers_bp.route("", methods=["GET"])
@limiter.limit("200 per day")
@token_required
def get_customer():
    customer_id = request.logged_in_id
    customer = db.session.get(Customer, customer_id)
    return customer_schema.jsonify(customer), 200


# get customers list
@customers_bp.route("/list", methods=["GET"])
@limiter.limit("200 per day")
@admin_or_tech_token_required
def get_customers():
    customers = db.session.query(Customer).all()
    return customers_schema.jsonify(customers), 200


# get customer by id. Admin and tech use only
@customers_bp.route("/<int:id>", methods=["GET"])
@limiter.limit("200 per day")
@admin_or_tech_token_required
def get_customer_by_id(id):
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"Error": "Customer not found"}), 404

    return customer_schema.jsonify(customer), 200


# delete customer by id
@customers_bp.route("/<int:id>", methods=["DELETE"])
@limiter.limit("5 per day")
@admin_token_required
def delete_customer(id):
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"Error": "Customer not found"}), 404

    db.session.delete(customer)
    db.session.commit()
    return jsonify({"Success": "Customer deleted"}), 200


# update customer
@customers_bp.route("", methods=["PUT"])
@limiter.limit("10 per day")
@token_required
def update_customer():
    customer_id = request.logged_in_id
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return jsonify({"Error": "Customer not found"}), 404

    try:
        data = customer_schema.load(request.json, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    if "password" in data:
        data["password"] = generate_password_hash(data["password"])
    # )  # resetting the password key's value, to the hash of the current value

    for key, value in data.items():
        setattr(customer, key, value)

    db.session.commit()
    return customer_schema.jsonify(customer), 200


# update customer by id. Admin use only
@customers_bp.route("/<int:id>", methods=["PUT"])
@limiter.limit("10 per day")
@admin_token_required
def update_customer_by_id(id):
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"Error": "Customer not found"}), 404

    try:
        data = customer_schema.load(request.json, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    if "password" in data:
        data["password"] = generate_password_hash(data["password"])
    # )  # resetting the password key's value, to the hash of the current value

    for key, value in data.items():
        setattr(customer, key, value)

    db.session.commit()
    return customer_schema.jsonify(customer), 200
