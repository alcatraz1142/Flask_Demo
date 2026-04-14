
from flask import Blueprint, request, jsonify
import sqlite3
from security.auth import create_token
from security.passwords import verify_password

login_bp = Blueprint('login', __name__)

@login_bp.post('/login_vulnerable')
def login_vulnerable():
    data = request.get_json()

    username = data['username']
    password = data['password']

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()

    query = f"""
           SELECT id, username, password, role
           FROM users
           WHERE username = '{username}'
       """

    cursor.execute(query)
    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "Invalid credentials (vulnerable)"}), 401

    user_id, db_username, db_password_hash, role = row

    if not verify_password(password, db_password_hash):
        return jsonify({"error": "Invalid credentials (vulnerable)"}), 401

    token = create_token(user_id, db_username, role)
    return jsonify({'access_token': token, 'token_type': 'bearer'}), 200


@login_bp.post("/login_safe")
def login_safe():
    data = request.get_json()

    username = data['username']
    password = data['password']

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()

    query = """
     SELECT id, username, password, role
        FROM users
        WHERE username = ?
    """

    cursor.execute(query, (username,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "Invalid credentials (safe)"}), 401

    user_id, db_username, db_password_hash, role = row

    if not verify_password(password, db_password_hash):
        return jsonify({"error": "Invalid credentials (safe)"}), 401

    token = create_token(user_id, db_username, role)
    return jsonify({'access_token': token, 'token_type': 'bearer'}), 200






