import jwt
import functools
from flask import request, jsonify, g, current_app
from app.controllers.userController import get_user_by_id

def login_required(f):
    """
    Decorator to require authentication for protected routes.
    Extracts JWT token from Authorization header and validates it.
    """
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = get_user_by_id(data['user_id'])
            if not current_user:
                return jsonify({'error': 'Invalid token'}), 401
            g.user = current_user
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """
    Decorator to require admin privileges for protected routes.
    Checks if the current user has admin role.
    """
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        # First ensure user is logged in
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = get_user_by_id(data['user_id'])
            if not current_user:
                return jsonify({'error': 'Invalid token'}), 401
            
            # Check if user has admin role
            if not hasattr(current_user, 'role') or current_user.role != 'admin':
                return jsonify({'error': 'Admin privileges required'}), 403
            
            g.user = current_user
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    return decorated_function

def owner_required(f):
    """
    Decorator to require ownership of the resource.
    User can only access their own resources or admins can access all.
    """
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        # First ensure user is logged in
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = get_user_by_id(data['user_id'])
            if not current_user:
                return jsonify({'error': 'Invalid token'}), 401
            
            g.user = current_user
            
            # Check if user is admin (can access all resources)
            if hasattr(current_user, 'role') and current_user.role == 'admin':
                return f(*args, **kwargs)
            
            # For non-admin users, check ownership
            # This will be implemented in the specific route handlers
            return f(*args, **kwargs)
            
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
    return decorated_function

def get_current_user():
    """
    Helper function to get the current authenticated user from Flask's g object.
    """
    return getattr(g, 'user', None)

def check_resource_ownership(resource_user_id, current_user):
    """
    Helper function to check if current user owns the resource or is admin.
    """
    if hasattr(current_user, 'role') and current_user.role == 'admin':
        return True
    return current_user.id == resource_user_id 