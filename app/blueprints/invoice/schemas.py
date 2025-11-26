from app.extensions import ma
from app.models import Invoice


class InvoiceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Invoice
        include_fk = True


# Create instances of the schemas
invoice_schema = InvoiceSchema()
invoices_schema = InvoiceSchema(many=True)
