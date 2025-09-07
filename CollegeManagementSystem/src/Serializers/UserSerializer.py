class UserSerializer:
    @staticmethod
    def serialize(user):
        """Serialize a single user object to a dictionary."""
        if not user:
            return None
        
        # This serializer relies on the 'college' relationship in the User model
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role.value,
            "is_active": user.is_active,
            "college": {
                "id": user.college.college_id,
                "name": user.college.name
            } if user.college else None,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "last_login": user.last_login.isoformat() if user.last_login else None
        }

    @staticmethod
    def serialize_list(users):
        """Serialize a list of user objects."""
        return [UserSerializer.serialize(user) for user in users]
