from app.models import db, Invoice
from .schemas import invoice_schema, invoices_schema
from app.blueprints.invoice import invoices_bp
from flask import jsonify, request
from marshmallow import ValidationError
from app.extensions import limiter, cache
from werkzeug.security import check_password_hash, generate_password_hash
from app.util.auth import encode_token, token_required


# INVOICE ROUTES
# create invoice
@invoices_bp.route("", methods=["POST"])
@limiter.limit("5 per day")
@token_required
def create_invoice():
    try:
        data = invoice_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_invoice = Invoice(**data)
    db.session.add(new_invoice)
    db.session.commit()
    return invoice_schema.jsonify(new_invoice), 201


# get invoice by id
@invoices_bp.route("/<int:id>", methods=["GET"])
@limiter.limit("200 per day")
def get_invoice(id):
    invoice = db.session.get(Invoice, id)
    return jsonify(invoice_schema.dump(invoice)), 200


# get invoices
@invoices_bp.route("", methods=["GET"])
@limiter.limit("200 per day")
@cache.cached(timeout=500)
def get_invoices():
    invoices = db.session.query(Invoice).all()
    return jsonify(invoices_schema.dump(invoices)), 200


# delete invoices by id
@invoices_bp.route("/<int:id>", methods=["DELETE"])
@limiter.limit("5 per day")
@token_required
def delete_invoice(id):
    invoice = db.session.get(Invoice, id)
    if not invoice:
        return jsonify({"Error": "Invoice not found"}), 400

    db.session.delete(invoice)
    db.session.commit()
    return jsonify({"Success": "Invoice Deleted"}), 200


# update invoice by id
@invoices_bp.route("/<int:id>", methods=["PUT"])
@limiter.limit("10 per day")
@token_required
def update_invoice(id):
    invoice = db.session.get(Invoice, id)

    if not invoice:
        return jsonify({"Error": "Invoice not found"})

    try:
        data = invoice_schema.load(request.json, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    for key, value in data.items():
        setattr(invoice, key, value)

    db.session.commit()
    return invoice_schema.jsonify(invoice), 200
