from src.extensions import db
from datetime import datetime, timezone
import hashlib
from enum import Enum


class UserRole(Enum):
    USER = "USER"
    ADMIN = "ADMIN"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    college_id = db.Column(db.String(36), db.ForeignKey('colleges.college_id'), nullable=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100))
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.USER)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    last_login = db.Column(db.DateTime(timezone=True))
    
    def set_password(self, password):
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    def check_password(self, password):
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()
    def is_admin(self):
        return self.role == UserRole.ADMIN
    
    def __repr__(self):
        return f'<User {self.username} ({self.role.value})>'