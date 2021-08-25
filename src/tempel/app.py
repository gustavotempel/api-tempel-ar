from flask import Flask
from flask import jsonify
from flask import request

from dotenv import load_dotenv

load_dotenv()

import os
import sys

sys.path.append(os.environ["PYTHONPATH"])

from tempel.database import select_query
from tempel.database import modify_query


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def hello_world():
    return custom_response("Hello World!")


@app.route("/products", methods=["POST"])
def add_product():
    fields = ["name", "price", "url"]
    product_to_add = request.json
    values = ", ".join(str(add_single_quotes_to_str(product_to_add[field])) for field in fields)
    products_query = modify_query(f"INSERT INTO products ({', '.join(fields)}) VALUES ({values})")
    return custom_response("Product added")


@app.route("/products", methods=["GET"])
def get_products():
    fields = ["id", "name", "price", "url"]
    products_query = select_query(f"SELECT {', '.join(fields)} FROM products")
    products = list(filter(None, products_query)) if products_query else []
    product_list = []
    for product in products:
        product_list.append(dict(zip(fields, product)))
    return custom_response(jsonify(product_list))


@app.route("/products/<id>", methods=["GET"])
def get_product_by_id(id):
    fields = ["id", "name", "price", "url"]
    product_query = select_query(f"SELECT {', '.join(fields)} FROM products WHERE id={id}")
    product = dict(zip(fields, product_query[0])) if product_query else None
    return custom_response(jsonify(product))


@app.route("/products/<id>", methods=["DELETE"])
def delete_product_by_id(id):
    product_query = modify_query(f"DELETE FROM products WHERE id={id}")
    return custom_response("Product deleted")


@app.route("/products/<id>", methods=["PUT"])
def put_product_by_id(id):
    fields = ["name", "price", "url"]
    product_to_put = request.json
    values = ", ".join(str(add_single_quotes_to_str(product_to_put[field])) for field in fields)
    field_values = ", ".join(field + "=" + str(add_single_quotes_to_str(product_to_put[field])) for field in fields)
    product_query = modify_query(f"UPDATE products SET {field_values} WHERE id={id}")
    return custom_response("Product completely updated")


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


if __name__ == "__main__":
    app.run(debug=True)
