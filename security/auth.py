import os

import jwt
from datetime import datetime, timezone, timedelta
from flask import request, jsonify
from dotenv import load_dotenv

load_dotenv()

SECRET = os.getenv("JWT_SECRET", "default_secret_key")

def create_token(user_id: int, role: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,
        "role": role,
        "exp": now + timedelta(minutes=15),
        "iat": now
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")

def verify_token(token: str):
    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return None, "Missing Authorization Header"

    try:
        token = auth_header.split(" ")[1]
    except IndexError:
        return None, "Invalid Authorization Header Format"

    try:
        decoded = jwt.decode(token, SECRET, algorithms=["HS256"])
        return decoded, None

    except jwt.ExpiredSignatureError:
        return None, "Signature Expired"

    except jwt.InvalidTokenError:
        return None, "Invalid Token"









