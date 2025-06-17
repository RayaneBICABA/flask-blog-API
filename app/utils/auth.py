from flask import Blueprint, jsonify, request
from app.controllers.auth_controller import authenticate_user
from app.contorllers.userController import create_user

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    token, error = authenticate_user(email, password)
    if error:
        return jsonify({"error": error}), 401
    return jsonify({"token": token})

