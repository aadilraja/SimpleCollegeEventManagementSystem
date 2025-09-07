from src import UserSerializer

__all__ = ['RegistrationSerializer']

class RegistrationSerializer:
    @staticmethod
    def serialize(registration):
        return {
            "registration_id": registration.registration_id,
            "attended": registration.attended,
            "registered_at": registration.registered_at.isoformat(),
            "student": UserSerializer.serialize(registration.student) # Show who registered
        }
    
    @staticmethod
    def serialize_list(registrations):
        return [RegistrationSerializer.serialize(reg) for reg in registrations]