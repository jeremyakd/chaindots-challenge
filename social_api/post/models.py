from django.db import models
from user.models import User


class Post(models.Model):
    """Model for creating posts."""

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"Post by {self.author.username} at {self.created_at}"
