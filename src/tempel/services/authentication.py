import jwt
import os
import time

from functools import wraps
from http import HTTPStatus

from flask import request

from tempel.services import auth_controllers_bp


@auth_controllers_bp.route("/auth/token", methods=["POST"])
def authentication():
    if request.form["grant_type"] != "password":
        return {
            "error": "unsopported_grant_type",
            "error_description": "The authorization server does not support the requested 'grant_type'."
            }, HTTPStatus.BAD_REQUEST, {
                "Access-Control-Allow-Origin": "*"
                }

    username = request.form["username"]
    password = request.form["password"]
    expires_in = 300
    iat = int(time.time())
    exp = int(time.time()) + expires_in
    token = jwt.encode(payload={"username": username, "iat": iat, "exp": exp}, key=os.environ["SECRET_KEY"], algorithm="HS256")
    return {
        "access_token": token,
        "token_type": None,
        "expires_in": expires_in,
        "refresh_token": None,
        }, HTTPStatus.CREATED, {
            "Access-Control-Allow-Origin": "*"
            }


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
        else:
            return {"error": 401, "message": "No token provided"}, 401
        try:
            _ = jwt.decode(jwt=token, key=os.environ["SECRET_KEY"], algorithms="HS256")
        except:
            return {"error": 401, "message": "Token is invalid"}, 401
        return f(*args, **kwargs)
    return decorator
