import uuid
from datetime import datetime, UTC
from src.extensions import db
from sqlalchemy import UniqueConstraint

class Registration(db.Model):
    __tablename__ = 'registrations'

    registration_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    event_id = db.Column(db.String(36), db.ForeignKey('events.event_id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    attended = db.Column(db.Boolean, default=False, nullable=False)
    registered_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(UTC))

    __table_args__ = (UniqueConstraint('event_id', 'student_id', name='_event_student_uc'),)
    
    
    event = db.relationship('Event', back_populates='registrations')

    
    

    def __repr__(self):
        return f'<Registration {self.registration_id}>'