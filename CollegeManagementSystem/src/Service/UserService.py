from src import User, UserRole, db
from src.Entity.Colleges import College
from src.Utils.Logger import Logger
from datetime import datetime, timezone

class UserService:
    @staticmethod
    def get_all_users():
        try:
            return User.query.all()
        except Exception as e:
            Logger.error("Failed to fetch all users", e)
            raise

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)
        
    @staticmethod
    def get_users_by_role(role):
        return User.query.filter_by(role=role).all()

   
    @staticmethod
    def create_user(data):
        try:
            required_fields = ['username', 'email', 'password', 'full_name']
            for field in required_fields:
                if field not in data:
                    raise ValueError(f"Missing required field: {field}")
            
            college_id_to_assign = None
            college_name = data.get('college_name')

            if college_name:
                college = College.query.filter_by(name=college_name).first()
                
                if college:
                    college_id_to_assign = college.college_id
                else:
                    new_college = College(name=college_name)
                    db.session.add(new_college)
                    
                    db.session.flush()
                    college_id_to_assign = new_college.college_id
                    Logger.info(f"Created new college '{college_name}' with ID {college_id_to_assign}")

            role = UserRole.USER
            if 'role' in data and data['role']:
                try:
                    role = UserRole(data['role'].upper())
                except ValueError:
                    raise ValueError("Invalid role provided. Must be USER or ADMIN.")

            user = User(
                username=data['username'],
                email=data['email'],
                full_name=data['full_name'],
                role=role,
                college_id=college_id_to_assign 
            )
            user.set_password(data['password'])
            
            db.session.add(user)
            db.session.commit()
            Logger.info(f"Created new user: {user.username}")
            return user
        except Exception as e:
            Logger.error("Failed to create user", e)
            db.session.rollback()
            raise
    
    @staticmethod
    def get_user_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def update_last_login(user_id):
        user = User.query.get(user_id)
        if user:
            user.last_login = datetime.now(timezone.utc)
            db.session.commit()
            return user
        return None

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False
