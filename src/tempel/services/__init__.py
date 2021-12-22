from flask import Blueprint

auth_controllers_bp = Blueprint("auth_controllers", __name__)

from . import authentication