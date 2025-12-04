from datetime import datetime, timedelta, timezone
from jose import jwt
import jose
from functools import wraps
from flask import request, jsonify

SECRET_KEY = "super secret secrets"


def encode_token(customer_id, position=None):
    payload = {
        "exp": datetime.now(timezone.utc)
        + timedelta(days=0, hours=1),  # Set an expiration date of 1 hour from now
        "iat": datetime.now(timezone.utc),
        "sub": str(customer_id),  # VERY IMPORTANT, SET YOUR USER ID TO A STR
        "position": position,
        # "role": role,  # You will probably not have role unless you add it to your models
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def token_required(f):  # f stands for the function that is getting wrapped
    @wraps(f)
    def decoration(
        *args, **kwargs
    ):  # The function that runs before the functiuon that we're wrapping
        token = None

        if "Authorization" in request.headers:
            # Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjM1MTgwMTQsImlhdCI6MTc2MzUxNDQxNCwic3ViIjoiMSIsInJvbGUiOiJBZG1pbiJ9.2gEKkaU_LEQAxEPbj5734khp4k6jKMgJQsayui70iPw
            token = request.headers["Authorization"].split()[1]

        if not token:
            return jsonify({"error": "token missing from authorization headers"}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            print(data)
            request.logged_in_id = data["sub"]
        except jose.exceptions.ExpiredSignatureError:
            return jsonify({"message": "token is expired"}), 403
        except jose.exceptions.JWTError:
            return jsonify({"message": "invalid token"}), 401

        return f(*args, **kwargs)

    return decoration


def admin_token_required(f):  # f stands for the function that is getting wrapped
    @wraps(f)
    def decoration(
        *args, **kwargs
    ):  # The function that runs before the functiuon that we're wrapping
        token = None

        if "Authorization" in request.headers:
            # Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjM1MTgwMTQsImlhdCI6MTc2MzUxNDQxNCwic3ViIjoiMSIsInJvbGUiOiJBZG1pbiJ9.2gEKkaU_LEQAxEPbj5734khp4k6jKMgJQsayui70iPw
            token = request.headers["Authorization"].split()[1]

        if not token:
            return jsonify({"error": "token missing from authorization headers"}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            if data.get("position") != "admin":
                return jsonify({"message": "admin access required"}), 403
            print(data)
            request.logged_in_id = data["sub"]
        except jose.exceptions.ExpiredSignatureError:
            return jsonify({"message": "token is expired"}), 403
        except jose.exceptions.JWTError:
            return jsonify({"message": "invalid token"}), 401

        return f(*args, **kwargs)

    return decoration


def admin_or_tech_token_required(
    f,
):  # f stands for the function that is getting wrapped
    @wraps(f)
    def decoration(
        *args, **kwargs
    ):  # The function that runs before the functiuon that we're wrapping
        token = None

        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split()[1]

        if not token:
            return jsonify({"error": "token missing from authorization headers"}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            if data.get("position") not in ["admin", "tech", "manager"]:
                return jsonify({"message": "admin or tech access required"}), 403
            print(data)
            request.logged_in_id = data["sub"]
            request.logged_in_position = data["position"]
        except jose.exceptions.ExpiredSignatureError:
            return jsonify({"message": "token is expired"}), 403
        except jose.exceptions.JWTError:
            return jsonify({"message": "invalid token"}), 401

        return f(*args, **kwargs)

    return decoration
