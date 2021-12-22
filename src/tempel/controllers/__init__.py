from flask import Blueprint

product_controllers_bp = Blueprint("product_controllers", __name__)
user_controllers_bp = Blueprint("user_controllers", __name__)

from . import user_controllers, product_controllers