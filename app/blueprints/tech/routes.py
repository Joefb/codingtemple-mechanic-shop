from app.models import db, Tech
from .schemas import tech_schema, techs_schema, login_schema, create_tech_schema
from app.blueprints.tech import techs_bp
from flask import jsonify, request
from marshmallow import ValidationError
from app.extensions import limiter
from werkzeug.security import check_password_hash, generate_password_hash
from app.util.auth import (
    encode_token,
    admin_or_tech_token_required,
    admin_token_required,
)


## TEC ROUTES ##
# tech login
@techs_bp.route("/login", methods=["POST"])
@limiter.limit("5 per 10 minute")
def login():
    try:
        # get my user credentials - responsibility for my client
        data = login_schema.load(request.json)  # JSON -> Python
    except ValidationError as e:
        return jsonify(e.messages), 400

    tech = db.session.query(Tech).where(Tech.last_name == data["last_name"]).first()

    if tech and check_password_hash(tech.password, data["password"]):
        # Create token for tech
        token = encode_token(tech.id, tech.position)
        return jsonify(
            {
                "message": f"Welcome {tech.first_name}",
                "token": token,
            }
        ), 200


# create tech
@techs_bp.route("", methods=["POST"])
@limiter.limit("5 per day")
@admin_token_required
def create_tech():
    try:
        data = create_tech_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    data["password"] = generate_password_hash(
        data["password"]
    )  # resetting the password key's value, to the hash of the current value

    new_tech = Tech(**data)
    db.session.add(new_tech)
    db.session.commit()
    return create_tech_schema.jsonify(new_tech), 201


# get tech by id
@techs_bp.route("/<int:id>", methods=["GET"])
@limiter.limit("200 per day")
@admin_or_tech_token_required
def get_tech_by_id(id):
    tech = db.session.get(Tech, id)
    if not tech:
        return jsonify({"Error": "Tech not found"}), 404

    return tech_schema.jsonify(tech), 200


# get logged in tech
@techs_bp.route("", methods=["GET"])
@limiter.limit("200 per day")
@admin_or_tech_token_required
def get_tech():
    tech_id = request.logged_in_id
    tech = db.session.get(Tech, tech_id)
    return tech_schema.jsonify(tech), 200


# get techs list
@techs_bp.route("/list", methods=["GET"])
@limiter.limit("200 per day")
@admin_or_tech_token_required
def get_techs():
    techs = db.session.query(Tech).all()
    return jsonify(techs_schema.dump(techs, many=True)), 200


# delete tech by id
@techs_bp.route("/<int:id>", methods=["DELETE"])
@limiter.limit("5 per day")
@admin_token_required
def delete_tech(id):
    tech = db.session.get(Tech, id)
    if not tech:
        return jsonify({"Error": "Tech not found"}), 404

    db.session.delete(tech)
    db.session.commit()
    return jsonify({"Success": "Tech deleted"}), 200


# update tech
@techs_bp.route("", methods=["PUT"])
@limiter.limit("10 per day")
@admin_or_tech_token_required
def update_tech():
    tech_id = request.logged_in_id
    tech = db.session.get(Tech, tech_id)
    if not tech:
        return jsonify({"Error": "Tech not found"}), 404

    try:
        data = tech_schema.load(request.json, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    if "password" in data:
        data["password"] = generate_password_hash(data["password"])

    for key, value in data.items():
        setattr(tech, key, value)

    db.session.commit()
    return tech_schema.jsonify(tech), 200


# update tech by id admin only
@techs_bp.route("/<int:id>", methods=["PUT"])
@limiter.limit("10 per day")
@admin_token_required
def update_tech_by_id(id):
    tech = db.session.get(Tech, id)
    if not tech:
        return jsonify({"Error": "Tech not found"}), 404

    try:
        data = tech_schema.load(request.json, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    if "password" in data:
        data["password"] = generate_password_hash(data["password"])

    for key, value in data.items():
        setattr(tech, key, value)

    db.session.commit()
    return tech_schema.jsonify(tech), 200
