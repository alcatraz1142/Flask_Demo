import sqlite3

from flask import Blueprint, jsonify
from utils.token_required import token_required

secure_bp = Blueprint('secure', __name__)

@secure_bp.route('/secure', methods=['GET'])
@token_required
def secure_route(decoded_token):
    return jsonify({
        "message": "Access granted to secure endpoint",
        "user": decoded_token.get("username"),
        "role": decoded_token.get("role")
    }), 200


@secure_bp.route('/admin-only', methods=['GET'])
@token_required
def admin_only(decoded_token):
    if decoded_token.get("role") != "admin":
        return jsonify({"message": "Access denied"}), 403

    return jsonify({"message": "This is endpoint for admin only"})



@secure_bp.route('/user-vulnerable/<int:user_id>', methods=['GET'])
@token_required
def vulnerable_user(decoded_token, user_id):

    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, username, role FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({"message": "User not found"}), 404

    user_id, username, role = row
    return jsonify({
        "id": user_id,
        "username": username,
        "role": role
    })


@secure_bp.route('/user-safe/<int:user_id>', methods=['GET'])
@token_required
def user_secure(decoded_token, user_id):
    requester_id = int(decoded_token.get("sub"))
    requester_role = decoded_token.get("role")

    if requester_id != user_id and requester_role != "admin":
        return jsonify({"error": "Access denied"}), 403

    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({"message": "User not found"}), 404

    user_id, username, role = row
    return jsonify({
        "id": user_id,
        "username": username,
        "role": role
    })