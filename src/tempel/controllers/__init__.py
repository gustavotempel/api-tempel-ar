from flask import Blueprint

user_controllers_bp = Blueprint('user_controllers', __name__)

from . import user_controllers