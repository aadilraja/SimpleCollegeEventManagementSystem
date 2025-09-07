import uuid
from enum import Enum
from datetime import datetime, UTC
from src.extensions import db

# Using UUID for primary keys is excellent for scalability.
def generate_uuid():
    return str(uuid.uuid4())

class EventType(Enum):
    WORKSHOP = "Workshop"
    FEST = "Fest"
    SEMINAR = "Seminar"
    TECH_TALK = "Tech Talk"

class Event(db.Model):
    __tablename__ = 'events'
    event_id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    title = db.Column(db.String(150), nullable=False)
    type = db.Column(db.Enum(EventType), nullable=False)
    event_date = db.Column(db.DateTime(timezone=True), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(UTC)) # Added for consistency
    
    # Foreign Keys
    college_id = db.Column(db.String(36), db.ForeignKey('colleges.college_id'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    college = db.relationship('College', back_populates='events')
    creator = db.relationship('User', backref=db.backref('created_events', lazy=True))
    
    # --- START: Missing Relationship ---
    # This line creates the `event.registrations` attribute that was missing.
    # The `cascade` option ensures that if an event is deleted, all its registrations are also deleted.
    registrations = db.relationship('Registration', back_populates='event', lazy=True, cascade="all, delete-orphan")
    # --- END: Missing Relationship ---

    def __repr__(self):
        return f'<Event {self.title} ({self.type.value})>'