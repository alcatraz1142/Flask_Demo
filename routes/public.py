from flask import Blueprint, jsonify

public_bp = Blueprint('public', __name__)

@public_bp.route('/public', methods=['GET'])
def public():
    return jsonify({'message': 'Public endpoint - no authentication required'})

