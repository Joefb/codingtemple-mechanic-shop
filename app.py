from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Float, ForeignKey, Table, Column, Date
from datetime import date
from flask_marshmallow import Marshmallow  # Importing Marshmallow class
from marshmallow import ValidationError

# Create Flask application instance
app = Flask(__name__)

# Connect to database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"


# Create a bass class for our models
class Base(DeclarativeBase):
    pass


# Create a instance of the database
db = SQLAlchemy(model_class=Base)

# Init Marshmallow with the Flask app
ma = Marshmallow()

# Init the extension onto the Flask app
db.init_app(app)  # This adds the db to the app.
ma.init_app(app)  # This adds Marshmallow to the app.

# Create association table for many-to-many relationship between Tech and Invoice
tech_invoices = Table(
    "tech_invoices",
    Base.metadata,
    Column("tech_id", ForeignKey("techs.id")),
    Column("invoice_id", ForeignKey("invoices.id")),
)


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    address: Mapped[str] = mapped_column(String(200), nullable=False)

    # Create relationship to Invoice
    invoices: Mapped[list["Invoice"]] = relationship(
        "Invoice", back_populates="customer"
    )


class Invoice(Base):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(200), nullable=False)
    total_cost: Mapped[float] = mapped_column(Float, nullable=False)
    vehicle: Mapped[str] = mapped_column(String(200), nullable=False)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)

    # Create relationship to Customer and techs
    customer: Mapped["Customer"] = relationship("Customer", back_populates="invoices")
    techs: Mapped[list["Tech"]] = relationship(
        "Tech", secondary="tech_invoices", back_populates="invoices"
    )


class Tech(Base):
    __tablename__ = "techs"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    position: Mapped[str] = mapped_column(String(50), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)

    # create relationship to invoice
    invoices: Mapped[list["Invoice"]] = relationship(
        "Invoice", secondary="tech_invoices", back_populates="techs"
    )


# Create schemas for serialization
class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer


class InvoiceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Invoice


class TechSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tech


# Create instances of the schemas
customer_schema = CustomerSchema()
invoice_schema = InvoiceSchema()
tech_schema = TechSchema()


### ROUTES ###


# CUSTOMER ROUTES
# creat customer
@app.route("/customer", methods=["POST"])
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
@app.route("/customer/<int:id>", methods=["GET"])
def get_customer(id):
    customer = db.session.get(Customer, id)
    return customer_schema.jsonify(customer), 200


with app.app_context():
    db.create_all()  # Create the database and the database table(s)


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
