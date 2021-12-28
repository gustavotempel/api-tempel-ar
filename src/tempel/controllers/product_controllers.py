import json
from http import HTTPStatus

from flask import abort, current_app, request
from sqlalchemy.exc import IntegrityError

from tempel.controllers import product_controllers_bp
from tempel.domain import models
from tempel import codecs


marshaller = codecs.Marshaller()

@product_controllers_bp.route("/products", methods=["POST"])
def add_product():
    """
    Create product with the provided data.

    Returns:
        A Flask response.

    """
    try:
        product = json.loads(request.data)
        cmd = marshaller.marshall(product, models.Product)
        current_app.product_query_engine.add(cmd)
        return {"response": "ok"}, HTTPStatus.CREATED, {
            "Location": f"products/cmd.product_id",
            "Access-Control-Allow-Origin": "*"
            }
    except ValueError:
        return {
            "detail": "Request body is not valid JSON",
            "status": 400,
            "title": "Bad Request",
            }, HTTPStatus.BAD_REQUEST
    except TypeError:
        return {
            "detail": "Request body is not valid",
            "status": 400,
            "title": "Bad Request",
            }, HTTPStatus.BAD_REQUEST
    except IntegrityError:
        return {
            "detail": "Product id already exists",
            "status": 400,
            "title": "Bad Request",
            }, HTTPStatus.BAD_REQUEST
    except Exception as err:
        return {
            "detail": f"Unexpected {err=}",
            "status": 400,
            "title": "Bad Request",
            }, HTTPStatus.BAD_REQUEST


@product_controllers_bp.route("/products", methods=["GET"])
def search_products():
    """
    Get product list.

    Returns:
        A Flask response.

    """
    result = current_app.product_query_engine.search()
    product_list = list(
        {
            k: v
            for k, v in {
                "product_id": product.product_id,
                "name": product.name,
                "price": product.price,
                "image": product.image,
            }.items()
        } for product in result
    )
    return {
        "result": product_list,
        "total": len(result),
    }, HTTPStatus.OK, {
        "Access-Control-Allow-Origin": "*"
        }


@product_controllers_bp.route("/products/<id>", methods=["GET"])
def get_product_by_id(id):
    """
    Get product by id.

    Returns:
        A Flask response.    

    """
    try:
        product_id = int(id)
    except ValueError:
        abort(HTTPStatus.BAD_REQUEST)
    result = current_app.product_query_engine.get(product_id)
    if not result:
        abort(HTTPStatus.NOT_FOUND)
    return {
        k: v
        for k, v in {
            "product_id": result.product_id,
            "name": result.name,
            "price": result.price,
            "image": result.image,
        }.items()
    }, HTTPStatus.OK, {
        "Access-Control-Allow-Origin": "*"
        }


@product_controllers_bp.route("/products/<id>", methods=["PUT"])
def update_product(id):
    """
    Update product with the provided data.

    Returns:
        A Flask response.

    """
    try:
        product_id = int(id)
    except ValueError:
        abort(HTTPStatus.BAD_REQUEST)
    product = current_app.product_query_engine.get(product_id)
    if not product:
        abort(HTTPStatus.NOT_FOUND)
    try:
        new_product = json.loads(request.data)
        cmd = marshaller.marshall(new_product, models.Product)
        current_app.product_query_engine.update(product_id, new_product)
        return {"id": cmd.product_id}, HTTPStatus.CREATED, {"Location": f"products/{cmd.product_id}"}
    except ValueError:
        return {
            "detail": "Request body is not valid JSON",
            "status": 400,
            "title": "Bad Request",
            }, HTTPStatus.BAD_REQUEST
    except TypeError:
        return {
            "detail": "Request body is not valid",
            "status": 400,
            "title": "Bad Request",
            }, HTTPStatus.BAD_REQUEST
    except IntegrityError:
        return {
            "detail": "Product id already exists",
            "status": 400,
            "title": "Bad Request",
            }, HTTPStatus.BAD_REQUEST
    except Exception as err:
        return {
            "detail": f"Unexpected {err=}",
            "status": 400,
            "title": "Bad Request",
            }, HTTPStatus.BAD_REQUEST


@product_controllers_bp.route("/products/<id>", methods=["DELETE"])
def delete_product(id):
    """
    Given an id, removes the product from the database.

    Returns:
        A Flask response.

    """
    try:
        product_id = int(id)
    except ValueError:
        abort(HTTPStatus.BAD_REQUEST)
    product = current_app.product_query_engine.get(product_id)
    if not product:
        abort(HTTPStatus.NOT_FOUND)
    try:
        current_app.product_query_engine.delete(product_id)
        return {"result": "Product deleted successfully"}, HTTPStatus.OK
    except ValueError:
        return {
            "detail": "Request body is not valid JSON",
            "status": 400,
            "title": "Bad Request",
            }, HTTPStatus.BAD_REQUEST
    except TypeError:
        return {
            "detail": "Request body is not valid",
            "status": 400,
            "title": "Bad Request",
            }, HTTPStatus.BAD_REQUEST
    except IntegrityError:
        return {
            "detail": "Product id already exists",
            "status": 400,
            "title": "Bad Request",
            }, HTTPStatus.BAD_REQUEST
    except Exception as err:
        return {
            "detail": f"Unexpected {err=}",
            "status": 400,
            "title": "Bad Request",
            }, HTTPStatus.BAD_REQUEST
