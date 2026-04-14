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
