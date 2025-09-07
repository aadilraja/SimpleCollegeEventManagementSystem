# app.py
from flask import Flask
from datetime import timedelta
import os
from src.Controller.UserController import user_bp
from src.Controller.EventController import event_bp
from src import db, User, UserRole

def create_app():
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET', 'cg54nuXohCe7lQubX1KqCXyJ-ck6V_ZI28pPQo7k033oB92l0O_xoSbV5OAJyDVn7ym3F_j4297ieesL3z0aSw==')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 

    # Initialize the database with the app
    db.init_app(app)

    # Register the blueprints
    app.register_blueprint(user_bp)
    app.register_blueprint(event_bp)
    
    return app

def initialize_database(app):
    with app.app_context():
        db.create_all()
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                email='admin@example.com',
                full_name='Administrator',
                role=UserRole.ADMIN
            )
            admin_user.set_password('admin123')
            
            db.session.add(admin_user)
            db.session.commit()
            print("Default admin user created!")
        else:
            print("Admin user already exists!")
        
        
        print("Database initialized!")

if __name__ == '__main__':
    app = create_app()
    initialize_database(app)
    app.run(debug=True)
