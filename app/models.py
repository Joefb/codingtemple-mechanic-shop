from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Float, ForeignKey, Table, Column, Date
from datetime import date


# Create a base class for our models
class Base(DeclarativeBase):
    pass


# Create a instance of the database
db = SQLAlchemy(model_class=Base)


# MODELS
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
    date: Mapped[date] = mapped_column(Date, nullable=False)  # Format YYYY-MM-DD
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
