from app.extensions import ma
from app.models import Tech


class TechSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tech


tech_schema = TechSchema()
techs_schema = TechSchema(many=True)
login_schema = TechSchema(only=("last_name", "password"))
