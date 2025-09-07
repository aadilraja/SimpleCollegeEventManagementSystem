from src.Entity.Event import Event, EventType
from src.Entity.Colleges import College
from src.Entity.Registeration import Registration
from src import User, UserRole
from src.extensions import db
from datetime import datetime
from src.Utils.Logger import Logger # Added for logging new college creation

class EventService:
    @staticmethod
    def create_event(data, admin_id):
        """
        Creates a new event. If the specified college does not exist,
        it creates a new one.
        """
        required_fields = ['title', 'type', 'event_date', 'college_name']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        # --- START: Updated "Find or Create" College Logic ---
        college_name = data['college_name']
        college = College.query.filter_by(name=college_name).first()

        if not college:
            college = College(name=college_name)
            db.session.add(college)
            db.session.flush()
            Logger.info(f"Created new college '{college.name}' with ID {college.college_id}")

        try:
            event_type = EventType[data['type'].upper().replace(" ", "_")]
        except KeyError:
            valid_types = [t.name for t in EventType]
            raise ValueError(f"Invalid event type. Must be one of: {valid_types}")
        
        # Validate and parse date
        try:
            event_date = datetime.fromisoformat(data['event_date'].replace('Z', '+00:00'))
        except (ValueError, TypeError):
            raise ValueError("Invalid event_date format. Please use ISO 8601 format.")

        # Create the event using the found or newly created college's ID
        new_event = Event(
            title=data['title'],
            type=event_type,
            event_date=event_date,
            college_id=college.college_id, # This now works for both existing and new colleges
            created_by=admin_id
        )
        
        db.session.add(new_event)
        db.session.commit()
        Logger.info(f"Created new event '{new_event.title}' for college '{college.name}'")
        return new_event

    @staticmethod
    def get_all_events():
        return Event.query.order_by(Event.event_date.asc()).all()

    @staticmethod
    def get_event_by_id(event_id):
        return Event.query.get(event_id)

    @staticmethod
    def register_for_event(event_id, student_id):
        event = Event.query.get(event_id)
        if not event:
            raise ValueError(f"Event with ID {event_id} not found.")

        student = User.query.get(student_id)
        if not student or student.role != UserRole.USER:
            raise ValueError("User not found or is not a student.")

        existing_reg = Registration.query.filter_by(event_id=event_id, student_id=student_id).first()
        if existing_reg:
            raise ValueError("Student is already registered for this event.")
        
        new_registration = Registration(event_id=event_id, student_id=student_id)
        db.session.add(new_registration)
        db.session.commit()
        
        return new_registration
    
    @staticmethod
    def update_event(event_id, data):
        event = Event.query.get(event_id)
        if not event:
            raise ValueError("Event not found.")

        # Update simple fields
        if 'title' in data:
            event.title = data['title']
        if 'type' in data:
            try:
                event.type = EventType[data['type'].upper().replace(" ", "_")]
            except KeyError:
                raise ValueError("Invalid event type.")
        if 'event_date' in data:
            try:
                event.event_date = datetime.fromisoformat(data['event_date'].replace('Z', '+00:00'))
            except (ValueError, TypeError):
                raise ValueError("Invalid event_date format.")

        db.session.commit()
        return event

    @staticmethod
    def delete_event(event_id):
        """Deletes an event and all its associated registrations."""
        event = Event.query.get(event_id)
        if not event:
            raise ValueError("Event not found.")
        
        db.session.delete(event)
        db.session.commit()
        return True

    @staticmethod
    def mark_attendance(registration_id):
        """Marks a student's registration as attended."""
        registration = Registration.query.get(registration_id)
        if not registration:
            raise ValueError("Registration not found.")
        
        registration.attended = True
        db.session.commit()
        return registration
        