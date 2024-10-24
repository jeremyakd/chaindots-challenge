from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, db_index=True)
    username = models.CharField(
        max_length=100,
        blank=True,
        unique=True,
        db_index=True,
    )
    password = models.CharField(max_length=128, blank=True)
    followers = models.ManyToManyField(
        "self", symmetrical=False, related_name="following", blank=True
    )

    def follow(self, user):
        """Follow another user"""
        self.following.add(user)

    def unfollow(self, user):
        """Unfollow another user"""
        self.following.remove(user)

    def is_following(self, user):
        """Check if following another user"""
        return self.following.filter(pk=user.pk).exists()

    def is_followed_by(self, user):
        """Check if followed by another user"""
        return self.followers.filter(pk=user.pk).exists()
