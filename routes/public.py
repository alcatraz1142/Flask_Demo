import html
from flask import Blueprint, jsonify, request

public_bp = Blueprint('public', __name__)

@public_bp.route('/public', methods=['GET'])
def public():
    return jsonify({'message': 'Public endpoint - no authentication required'})

@public_bp.route('/xss-vulnereable', methods=['GET'])
def xss_vulnereable():
    value = request.args.get("q", "")
    #zwrócenie wartości bez żadnej walidacji
    return f"<h1>Echo: {value}</h1>"

@public_bp.route('/xss-safe', methods=['GET'])
def xss_safe():
    value = request.args.get("q", "")
    safe_value = html.escape(value)
    return f"<h1>Echo: {safe_value}</h1>"
