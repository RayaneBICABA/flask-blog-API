from flask import Blueprint, jsonify, request
from app.controllers.userController import (
    get_all_users, get_user_by_id, update_user, delete_user
)
from app.utils.auth import login_required, admin_required

user_bp = Blueprint('user', __name__, url_prefix='/api/users')

@user_bp.route('/', methods=['GET'])
@admin_required
def get_users():
    users = get_all_users()
    return jsonify([user.to_dict() for user in users])