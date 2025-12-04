from app.extensions import ma
from app.models import Tech


class TechSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tech


class PublicTechSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tech
        exclude = ("password",)


tech_schema = PublicTechSchema()
create_tech_schema = TechSchema()
techs_schema = PublicTechSchema(many=True)
login_schema = TechSchema(only=("last_name", "password"))
