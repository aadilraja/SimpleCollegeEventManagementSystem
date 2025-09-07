# controllers/UserController.py

from flask import Blueprint, request, jsonify, current_app
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import jwt

# Import services and serializers
from src import (
    UserService,
    UserSerializer,
    UserRole,
    generate_access_token,
    generate_refresh_token,
    jwt_required,
    admin_required
)
from src.Utils.Logger import Logger

user_bp = Blueprint('users', __name__, url_prefix='/users')

# Add make_response to your imports from flask
from flask import Blueprint, request, jsonify, make_response


@user_bp.route('/login', methods=['POST'])
def login_endpoint():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"success": False, "error": "Username and password are required"}), 400
        
    username = data.get('username')
    password = data.get('password')

    user = UserService.get_user_by_username(username) or UserService.get_user_by_email(username)

    if not user or not user.check_password(password):
        return jsonify({"success": False, "error": "Invalid credentials"}), 401
        
    if not user.is_active:
        return jsonify({"success": False, "error": "Account is inactive"}), 403

    UserService.update_last_login(user.id)
    
    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)
    
   
    response_body = {
        "success": True,
        "message": "Login successful",
        "data": {
            "user": UserSerializer.serialize(user)
        }
    }
    
    resp = make_response(jsonify(response_body), 200)
    
    resp.set_cookie(
        'access_token',
        value=access_token,
        httponly=True,        
        secure=True,          
        samesite='Lax'       
    )
    resp.set_cookie(
        'refresh_token',
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite='Lax'
    )
    
    return resp
@user_bp.route('/refresh', methods=['POST'])
def refresh_token_endpoint():
    data = request.get_json()
    refresh_token = data.get('refresh_token')
    if not refresh_token:
        return jsonify({"success": False, "error": "Refresh token is required"}), 400
    
    try:
        payload = jwt.decode(refresh_token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        if payload.get('type') != 'refresh':
            raise jwt.InvalidTokenError("Invalid token type")

        user = UserService.get_user_by_id(payload['user_id'])
        if not user or not user.is_active:
            return jsonify({"success": False, "error": "User not found or inactive"}), 401
            
        access_token = generate_access_token(user)
        return jsonify({"success": True, "access_token": access_token}), 200
        
    except jwt.ExpiredSignatureError:
        return jsonify({"success": False, "error": "Refresh token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"success": False, "error": "Invalid refresh token"}), 401

# --- PROTECTED ROUTES ---

# In your UserController.py, make sure you import 'make_response'
from flask import Blueprint, request, jsonify, make_response


@user_bp.route('/logout', methods=['POST'])
@jwt_required 
def logout_endpoint():
   
    resp = make_response(jsonify({
        "success": True,
        "message": "Logout successful"
    }), 200)
    
   
    resp.set_cookie('access_token', value='', expires=0, httponly=True, secure=True, samesite='Lax')
    resp.set_cookie('refresh_token', value='', expires=0, httponly=True, secure=True, samesite='Lax')
    
    return resp

@user_bp.route('/profile', methods=['GET'])
@jwt_required
def get_profile_endpoint():
    user = request.current_user
    return jsonify({
        "success": True,
        "data": UserSerializer.serialize(user)
    }), 200

# --- ADMIN-PROTECTED ROUTES ---

@user_bp.route('', methods=['GET'])
@admin_required
def get_all_users_endpoint():
    users = UserService.get_all_users()
    return jsonify({
        "success": True,
        "data": UserSerializer.serialize_list(users),
        "count": len(users)
    }), 200
    

@user_bp.route('/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user_endpoint(user_id):
    if user_id == request.current_user.id:
        return jsonify({"success": False, "error": "Admin cannot delete themselves"}), 403

    success = UserService.delete_user(user_id)
    if not success:
        return jsonify({"success": False, "error": "User not found"}), 404
        
    return jsonify({"success": True, "message": "User deleted successfully"}), 200

# --- ADMIN-PROTECTED ROUTES Ends---

@user_bp.route('', methods=['POST'])
def create_user_endpoint():
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400
        
        user = UserService.create_user(data)
        
        return jsonify({
            "success": True,
            "message": "User created successfully",
            "data": UserSerializer.serialize(user)
        }), 201
        
    except ValueError as e:
        Logger.error(f"Validation error in create_user: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 400
    except IntegrityError as e:
        Logger.error(f"Integrity error in create_user: {str(e)}")
        return jsonify({"success": False, "error": "Username or email already exists"}), 409
    except Exception as e:
        Logger.error(f"Unexpected error in create_user: {str(e)}")
        return jsonify({"success": False, "error": "Internal server error"}), 500
