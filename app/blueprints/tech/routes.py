from app.models import db, Tech
from .schemas import tech_schema, techs_schema
from app.blueprints.tech import techs_bp
from flask import jsonify, request
from marshmallow import ValidationError
from app.extensions import limiter, cache


## TEC ROUTES ##
# create tech
@techs_bp.route("", methods=["POST"])
@limiter.limit("5 per day")
def create_tech():
    try:
        data = tech_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_tech = Tech(**data)
    db.session.add(new_tech)
    db.session.commit()
    return tech_schema.jsonify(new_tech), 201


# get tech by id
@techs_bp.route("/<int:id>", methods=["GET"])
@limiter.limit("200 per day")
def get_tech(id):
    tech = db.session.get(Tech, id)
    return tech_schema.jsonify(tech), 200


# get techs list
@techs_bp.route("", methods=["GET"])
@limiter.limit("200 per day")
def get_techs():
    techs = db.session.query(Tech).all()
    return jsonify(techs_schema.dump(techs, many=True)), 200


# delete tech by id
@techs_bp.route("/<int:id>", methods=["DELETE"])
@limiter.limit("5 per day")
def delete_tech(id):
    tech = db.session.get(Tech, id)
    if not tech:
        return jsonify({"Error": "Tech not found"}), 404


# TODO: update tech by id
# @techs_bp.route("/<int:id>", methods=["PUT"])
