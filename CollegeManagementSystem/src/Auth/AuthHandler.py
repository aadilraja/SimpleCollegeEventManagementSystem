import jwt
# Use the modern, timezone-aware UTC object
from datetime import datetime, UTC
from functools import wraps
from flask import request, jsonify, current_app

from src import UserService

# --- Token Generation (Updated to use modern datetime) ---

def generate_access_token(user):
    """Generate JWT access token for a user."""
    payload = {
        'user_id': user.id,
        'username': user.username,
        'role': user.role.value,
        'type': 'access',
        'iat': datetime.now(UTC),
        'exp': datetime.now(UTC) + current_app.config['JWT_ACCESS_TOKEN_EXPIRES']
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

def generate_refresh_token(user):
    """Generate JWT refresh token for a user."""
    payload = {
        'user_id': user.id,
        'type': 'refresh',
        'iat': datetime.now(UTC),
        'exp': datetime.now(UTC) + current_app.config['JWT_REFRESH_TOKEN_EXPIRES']
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

# --- Decorators (Updated to use cookies) ---

def jwt_required(f):
    """
    Decorator to protect routes by checking for a JWT in an HttpOnly cookie.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 1. Get the token from the cookie named 'access_token'
        token = request.cookies.get('access_token')
        
        if not token:
            return jsonify({"success": False, "error": "Authentication token is missing"}), 401
        
        try:
            # 2. Decode the token (no need to split 'Bearer')
            payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            
            if payload.get('type') != 'access':
                return jsonify({"success": False, "error": "Invalid token type"}), 401
            
            # 3. Find the user based on the token payload
            user = UserService.get_user_by_id(payload['user_id'])
            if not user or not user.is_active:
                return jsonify({"success": False, "error": "User not found or inactive"}), 401
            
            # 4. Attach the user object to the request context
            request.current_user = user
            
        except jwt.ExpiredSignatureError:
            return jsonify({"success": False, "error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"success": False, "error": "Invalid token"}), 401
        
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """
    Decorator to ensure the user has an admin role.
    This decorator works without changes because it's stacked on top of
    the updated jwt_required, which correctly populates request.current_user.
    """
    @wraps(f)
    @jwt_required # Ensures jwt_required runs first to check the cookie
    def decorated_function(*args, **kwargs):
        if not request.current_user.is_admin():
            return jsonify({"success": False, "error": "Admin access required"}), 403
        return f(*args, **kwargs)
    return decorated_function
