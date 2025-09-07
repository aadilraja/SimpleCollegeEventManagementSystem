from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src import EventService
from src import EventSerializer
from src import RegistrationSerializer
from src.Utils.Logger import Logger
from src import (
    admin_required,
    jwt_required
)    

event_bp = Blueprint('events', __name__, url_prefix='/events')

@event_bp.route('', methods=['POST'])
@admin_required
def create_event_endpoint():
   
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400
        
        # The admin's user object is attached to the request by the decorator
        admin_user = request.current_user
        
        event = EventService.create_event(data, admin_user.id)
        
        return jsonify({
            "success": True,
            "message": "Event created successfully",
            "data": EventSerializer.serialize(event)
        }), 201

    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": "An internal error occurred"}), 500



@event_bp.route('', methods=['GET'])
@jwt_required
def get_all_events():
    """Get a list of all upcoming events."""
    try:
        events = EventService.get_all_events()
        return jsonify({
            "success": True,
            "data": EventSerializer.serialize_list(events)
        }), 200
    except Exception as e:
        Logger.error("Failed to retrieve events", e)
        return jsonify({"success": False, "error": "An unexpected error occurred."}), 500

@event_bp.route('/<event_id>', methods=['GET'])
@jwt_required
def get_event_details(event_id):
    """Get detailed information about a single event."""
    try:
        include_registrations = request.current_user.is_admin()
        event = EventService.get_event_by_id(event_id)
        if not event:
            return jsonify({"success": False, "error": "Event not found"}), 404
        
        return jsonify({
            "success": True,
            "data": EventSerializer.serialize(event, include_registrations=include_registrations)
        }), 200
    except Exception as e:
        Logger.error(f"Failed to retrieve details for event {event_id}", e)
        return jsonify({"success": False, "error": "An unexpected error occurred."}), 500
    

@event_bp.route('/<event_id>/register', methods=['POST'])
@jwt_required
def register_for_event(event_id):
    """Register the current user for an event."""
    student_id = request.current_user.id
    try:
        registration = EventService.register_for_event(event_id, student_id)
        return jsonify({
            "success": True,
            "message": "Successfully registered for the event.",
            "data": { "registration_id": registration.registration_id }
        }), 201
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except IntegrityError:
        return jsonify({"success": False, "error": "Student is already registered for this event."}), 409
    except Exception as e:
        Logger.error(f"Failed to register user {student_id} for event {event_id}", e)
        return jsonify({"success": False, "error": "An unexpected error occurred."}), 500
    
    
    
@event_bp.route('/<event_id>', methods=['PUT'])
@admin_required
def update_event(event_id):
    """Update an event's details (admin only)."""
    data = request.get_json()
    try:
        updated_event = EventService.update_event(event_id, data)
        return jsonify({
            "success": True,
            "message": "Event updated successfully.",
            "data": EventSerializer.serialize(updated_event, include_registrations=True)
        }), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404
    except Exception as e:
        Logger.error(f"Failed to update event {event_id}", e)
        return jsonify({"success": False, "error": "An unexpected error occurred."}), 500

@event_bp.route('/<event_id>', methods=['DELETE'])
@admin_required
def delete_event(event_id):
    """Delete an event (admin only)."""
    try:
        EventService.delete_event(event_id)
        return jsonify({
            "success": True,
            "message": "Event deleted successfully."
        }), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404
    except Exception as e:
        Logger.error(f"Failed to delete event {event_id}", e)
        return jsonify({"success": False, "error": "An unexpected error occurred."}), 500
    

@event_bp.route('/dashboard', methods=['GET'])
@admin_required
def get_admin_event_dashboard():
    """Get all events with full registration details for admins."""
    try:
        events = EventService.get_all_events()
        # The serializer needs to be passed the flag to include registrations
        return jsonify({
            "success": True,
            "data": EventSerializer.serialize_list(events, include_registrations=True)
        }), 200
    except Exception as e:
        Logger.error("Failed to retrieve admin event dashboard", e)
        return jsonify({"success": False, "error": "An unexpected error occurred."}), 500

@event_bp.route('/registrations/<registration_id>/check-in', methods=['POST'])
@admin_required
def mark_attendance(registration_id):
    """Mark a student as attended for an event (admin check-in)."""
    try:
        updated_registration = EventService.mark_attendance(registration_id)
        return jsonify({
            "success": True,
            "message": "Attendance marked successfully.",
            "data": RegistrationSerializer.serialize(updated_registration)
        }), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404
    except Exception as e:
        Logger.error(f"Failed to mark attendance for registration {registration_id}", e)
        return jsonify({"success": False, "error": "An unexpected error occurred."}), 500


