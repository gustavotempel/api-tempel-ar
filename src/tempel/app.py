from flask import Flask
from flask import jsonify
from flask import request

from flask_swagger_ui import get_swaggerui_blueprint

from functools import wraps

from dotenv import load_dotenv

load_dotenv()

import os
import sys
import jwt
import time

sys.path.append(os.environ["PYTHONPATH"])

from tempel.database import select_query
from tempel.database import modify_query

SWAGGER_URL = "/api/docs"
API_URL = "/static/openapi.yml"

app = Flask(__name__)

app.secret_key = os.environ["SECRET_KEY"]


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if "access_token" in request.headers:
            token = request.headers["access_token"]
        else:
            return {"error": 401, "message": "No token provided"}, 401
        try:
            data = jwt.decode(token, app.secret_key, algorithms="HS256")
        except:
            return {"error": 401, "message": "Token is invalid"}, 401
        return f(*args, **kwargs)
    return decorator


@app.route("/auth/token", methods=["POST"])
def authentication():
    if request.form["grant_type"] == "password":
        username = request.form["username"]
        password = request.form["password"]
        expires_in = 300
        iat = int(time.time())
        exp = int(time.time()) + expires_in
        token = jwt.encode({"username": username, "iat": iat, "exp": exp}, app.secret_key, algorithm="HS256")
        return custom_response(
            {
            "access_token": token,
            "token_type": None,
            "expires_in": expires_in,
            "refresh_token": None,
            }, 200)
    return custom_response({"error": "unsopported_grant_type", "error_description": "The authorization server does not support the requested 'grant_type'."}, 400)


@app.route("/", methods=["GET", "POST"])
def index():
    return custom_response(f"<a href={SWAGGER_URL}>See the documentation!<a>")


@app.route("/product/<id>", methods=["GET"])
@token_required
def search_product_by_id(id):
    fields = ["id", "name", "price", "url"]
    product_query = select_query(f"SELECT {', '.join(fields)} FROM products WHERE id={id}")
    product = dict(zip(fields, product_query[0])) if product_query else None
    return custom_response(jsonify(product))


@app.route("/product/<id>", methods=["DELETE"])
@token_required
def delete_product_by_id(id):
    product_query = modify_query(f"DELETE FROM products WHERE id={id}")
    return custom_response("Successfully deleted product", 202)


@app.route("/product/<id>", methods=["PUT"])
@token_required
def update_product_by_id(id):
    fields = ["name", "price", "url"]
    product_to_update = request.json
    values = ", ".join(str(add_single_quotes_to_str(product_to_update[field])) for field in fields)
    field_values = ", ".join(field + "=" + str(add_single_quotes_to_str(product_to_update[field])) for field in fields)
    product_query = modify_query(f"UPDATE products SET {field_values} WHERE id={id}")
    return custom_response("Successfully updated product")


@app.route("/product", methods=["GET"])
@token_required
def list_products():
    fields = ["id", "name", "price", "url"]
    products_query = select_query(f"SELECT {', '.join(fields)} FROM products")
    products = list(filter(None, products_query)) if products_query else []
    product_list = []
    for product in products:
        product_list.append(dict(zip(fields, product)))
    return custom_response(jsonify(product_list))


@app.route("/product", methods=["POST"])
@token_required
def add_product():
    fields = ["name", "price", "url"]
    product_to_add = request.json
    values = ", ".join(str(add_single_quotes_to_str(product_to_add[field])) for field in fields)
    products_query = modify_query(f"INSERT INTO products ({', '.join(fields)}) VALUES ({values})")
    return custom_response("Product added", 201)


def custom_response(body, code=None, headers=None):
    """Returns a tuple with body, code and/or headers"""
    if code is None:
        code = 200
    if headers is None:
        headers = {
            "Access-Control-Allow-Origin": "*"
            }
    return body, code, headers


def add_single_quotes_to_str(value):
    if isinstance(value, str):
        return f"'{value}'"
    return value


swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        "app_name": "Test application"
    },
)

app.register_blueprint(swaggerui_blueprint)


if __name__ == "__main__":
    app.run(debug=True)
