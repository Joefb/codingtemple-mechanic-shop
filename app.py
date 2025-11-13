from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String


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


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=False)
    dob: Mapped[str] = mapped_column(String(25), nullable=False)
    address: Mapped[str] = mapped_column(String(200), nullable=False)
    role: Mapped[str] = mapped_column(String(50))


with app.app_context():
    db.create_all()  # Create the database and the database table(s)


# Run the app
app.run()
