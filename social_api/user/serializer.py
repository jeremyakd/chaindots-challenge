from rest_framework import serializers
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the UserProfile model."""

    class Meta:
        model = User
        fields = ("id", "email", "username", "password", "followers")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data: dict) -> User:
        """Create a new user with encrypted password."""
        password: str | None = validated_data.pop("password", None)
        user: User = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
