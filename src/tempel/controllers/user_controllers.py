import json
from http import HTTPStatus

from flask import abort, current_app, request
from sqlalchemy.exc import IntegrityError

from tempel.controllers import user_controllers_bp
from tempel.domain import models
from tempel import codecs


marshaller = codecs.Marshaller()

@user_controllers_bp.route("/users", methods=["POST"])
def signup_user():
    """
    Create user with the provided data.
    
    Returns:
        A Flask response.

    """
    try:
        user = json.loads(request.data)
        cmd = marshaller.marshall(user, models.User)
        current_app.query_engine.add(cmd)
        return {"id": cmd.user_id}, HTTPStatus.CREATED, {"Location": f"users/{cmd.user_id}"}
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
            "detail": "Username or email already exists",
            "status": 400,
            "title": "Bad Request",
            }, HTTPStatus.BAD_REQUEST
    except:
        return {
            "detail": "Bad Request",
            "status": 400,
            "title": "Bad Request",
            }, HTTPStatus.BAD_REQUEST


@user_controllers_bp.route("/users", methods=["GET"])
def search_users():
    """
    Get user list.
    
    Returns:
        A Flask response.    

    """
    result = current_app.query_engine.search()
    user_list = list(
        {
            k: v
            for k, v in {
                "id": user.user_id,
                "username": user.username,
                "email": user.email,
                "is_active": user.is_active,
                "verified": user.verified,
            }.items()
        } for user in result
    )
    return {
        "result": user_list,
        "total": len(result),
    }


@user_controllers_bp.route("/users/<id>", methods=["GET"])
def get_user_by_id(id):
    """
    Get user by id.
    
    Returns:
        A Flask response.    

    """
    try:
        user_id = int(id)
    except ValueError:
        abort(HTTPStatus.BAD_REQUEST)
    result = current_app.query_engine.get(user_id)
    if not result:
        abort(HTTPStatus.NOT_FOUND)
    return {
        k: v
        for k, v in {
            "id": result.user_id,
            "username": result.username,
            "email": result.email,
            "is_active": result.is_active,
            "verified": result.verified,
        }.items()
    }