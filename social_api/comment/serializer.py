from comment.models import Comment
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for the Comment model."""

    class Meta:
        model = Comment
        fields = "__all__"
