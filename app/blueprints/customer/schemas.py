# Impopts
from app.extensions import ma
from app.models import Customer


# Create schemas for serialization
class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer


class PublicCustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        exclude = ("password",)


customer_schema = PublicCustomerSchema()
customers_schema = PublicCustomerSchema(many=True)
create_customer_schema = CustomerSchema()
login_schema = CustomerSchema(only=("email", "password"))
