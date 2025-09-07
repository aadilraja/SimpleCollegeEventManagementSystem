from src.extensions import db
import uuid

class College(db.Model):
    __tablename__ = 'colleges'
    college_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(150), unique=True, nullable=False)

    # Relationship to the users that belong to this college
    users = db.relationship('User', backref='college', lazy=True)
    
    # Relationship to the events hosted by this college
    events = db.relationship('Event', back_populates='college', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<College {self.name}>'
