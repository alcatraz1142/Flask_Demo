import logging
from functools import wraps
import jwt
from flask import request, jsonify, current_app

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            parts = request.headers['Authorization'].split(" ")
            if len(parts) == 2 and parts[0] == "Bearer":
                token = parts[1]

        if not token:
            logging.warning("Access denied: invalid or missing token")
            return jsonify({"message": "Token is missing"}), 401

        try:
            decoded = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],   # ← TU JEST ZMIANA
                algorithms=["HS256"]
            )
        except Exception:
            logging.warning("Access denied: invalid or missing token")
            return jsonify({"message": "Token is invalid"}), 401

        return f(decoded, *args, **kwargs)

    return decorated
