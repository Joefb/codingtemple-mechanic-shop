from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Float, ForeignKey, Table, Column, Date
from datetime import date


# Create Flask application instance
app = Flask(__name__)

# Connect to database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"


# Create a bass class for our models
class Base(DeclarativeBase):
    pass


# Create a instance of the database
db = SQLAlchemy(model_class=Base)

# Init the extension onto the Flask app
db.init_app(app)  # This adds the db to the app.

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
    invoice: Mapped[list["Invoice"]] = relationship(
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


with app.app_context():
    db.create_all()  # Create the database and the database table(s)


# Run the app
app.run()
