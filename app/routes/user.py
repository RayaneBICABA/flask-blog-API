from flask import Blueprint, jsonify, request, g
from app.controllers.userController import (
    get_all_users, get_user_by_id, update_user, delete_user, hard_delete_user,
    update_user_role, get_users_by_role
)
from app.utils.auth import login_required, admin_required, owner_required, check_resource_ownership

user_bp = Blueprint('user', __name__, url_prefix='/api/users')

@user_bp.route('/', methods=['GET'])
@admin_required
def get_users():
    """Get all active users (admin only)"""
    users = get_all_users()
    return jsonify([user.to_dict() for user in users])

@user_bp.route('/<int:user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    """Get user by ID (owner or admin only)"""
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Check if current user can access this user's data
    if not check_resource_ownership(user_id, g.user):
        return jsonify({'error': 'Access denied'}), 403
    
    return jsonify(user.to_dict())

@user_bp.route('/<int:user_id>', methods=['PUT'])
@login_required
def update_a_user(user_id):
    """Update user (owner or admin only)"""
    # Check if current user can update this user
    if not check_resource_ownership(user_id, g.user):
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    profile_image_url = data.get('profile_image_url')
    
    # Only admins can change roles
    role = None
    if g.user.is_admin() and 'role' in data:
        role = data.get('role')
    
    user = update_user(user_id, username, email, profile_image_url, role)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict())

@user_bp.route('/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_a_user(user_id):
    """Soft delete user (admin only)"""
    deleted = delete_user(user_id)
    if not deleted:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'message': 'User deleted'}), 200

@user_bp.route('/<int:user_id>/hard-delete', methods=['DELETE'])
@admin_required
def hard_delete_a_user(user_id):
    """Hard delete user (admin only)"""
    deleted = hard_delete_user(user_id)
    if not deleted:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'message': 'User permanently deleted'}), 200

@user_bp.route('/<int:user_id>/role', methods=['PUT'])
@admin_required
def update_user_role_endpoint(user_id):
    """Update user role (admin only)"""
    data = request.get_json()
    new_role = data.get('role')
    
    if not new_role or new_role not in ['user', 'admin']:
        return jsonify({'error': 'Invalid role. Must be "user" or "admin"'}), 400
    
    user = update_user_role(user_id, new_role)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict())

@user_bp.route('/role/<role>', methods=['GET'])
@admin_required
def get_users_by_role_endpoint(role):
    """Get users by role (admin only)"""
    if role not in ['user', 'admin']:
        return jsonify({'error': 'Invalid role. Must be "user" or "admin"'}), 400
    
    users = get_users_by_role(role)
    return jsonify([user.to_dict() for user in users])

@user_bp.route('/profile', methods=['GET'])
@login_required
def get_current_user_profile():
    """Get current user's profile"""
    return jsonify(g.user.to_dict())

@user_bp.route('/profile', methods=['PUT'])
@login_required
def update_current_user_profile():
    """Update current user's profile"""
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    profile_image_url = data.get('profile_image_url')
    
    user = update_user(g.user.id, username, email, profile_image_url)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict())