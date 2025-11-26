from flask import Blueprint

techs_bp = Blueprint("techs_bp", __name__)

from . import routes
