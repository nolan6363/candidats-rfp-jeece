from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from ..config import Config

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email', '')
    password = data.get('password', '')

    if email == Config.ADMIN_EMAIL and password == Config.ADMIN_PASSWORD:
        token = create_access_token(identity=email)
        return jsonify({'access_token': token})

    return jsonify({'error': 'Identifiants invalides'}), 401
