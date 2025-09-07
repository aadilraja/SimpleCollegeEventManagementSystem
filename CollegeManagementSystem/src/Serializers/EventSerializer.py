class EventSerializer:
    @staticmethod
    def serialize(event, include_registrations=False):
        """Serialize a single event object to a dictionary."""
        if not event:
            return None
        
        event_data = {
            "event_id": event.event_id,
            "title": event.title,
            "type": event.type.name,
            "event_date": event.event_date.isoformat(),
            "college_id": event.college_id,
            "created_by": event.created_by
        }
        
        if include_registrations:
            event_data["registrations"] = [
                {
                    "registration_id": reg.registration_id,
                    "student_id": reg.student_id,
                    "registration_date": reg.registration_date.isoformat()
                }
                for reg in event.registrations
            ]
            
        return event_data

    @staticmethod
    def serialize_list(events, include_registrations=False):
      
        return [EventSerializer.serialize(event, include_registrations=include_registrations) for event in events]

