from typing import Any, Dict, List, Optional

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from user.constants import ALREADY_FOLLOW, NEW_FOLLOW_MESSAGE, OWN_FOLLOW_ERROR
from user.models import User
from user.serializer import UserSerializer


class UserCreateAPIView(APIView):
    """
    API view to create a new user profile.
    Only accessible to authenticated users.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, format: Optional[str] = None) -> Response:
        """Create a new user profile with the data provided in the request."""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPIView(APIView):
    """
    API view to retrieve user details, including follower and post statistics.
    Only accessible to authenticated users.
    """

    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_post_count(user: User) -> int:
        """Return the total count of posts for the specified user."""
        return user.post_set.count()

    @staticmethod
    def get_comments_count(user: User) -> int:
        """Return the total count of comments for the specified user."""
        return user.comment_set.count()

    @staticmethod
    def get_followers(user: User) -> List[Dict[str, Any]]:
        """Return a list of followers for the specified user, serialized as JSON."""
        return UserSerializer(user.followers.all(), many=True).data

    @staticmethod
    def get_following(user: User) -> List[Dict[str, Any]]:
        """Return a list of users the specified user is following, serialized as JSON."""
        return UserSerializer(user.following.all(), many=True).data

    def get_user_data(self, user: User) -> Dict[str, Any]:
        """Aggregate user details, including follower and post statistics."""
        posts_count = self.get_post_count(user)
        comments_count = self.get_comments_count(user)
        followers = self.get_followers(user)
        following = self.get_following(user)

        serializer = UserSerializer(user)
        user_data = serializer.data
        user_data.update(
            {
                "total_posts": posts_count,
                "total_comments": comments_count,
                "followers": followers,
                "following": following,
            }
        )
        return user_data

    def get(self, request, user_id: int, format: Optional[str] = None) -> Response:
        """Retrieve the profile data of the specified user by user ID."""
        user = get_object_or_404(User, pk=user_id)
        user_data = self.get_user_data(user)
        return Response(user_data)


class UserCreateFollowAPIView(APIView):
    """
    API view to create a following relationship between two users.
    Only accessible to authenticated users.
    """

    permission_classes = [IsAuthenticated]

    def post(
        self, request, follower_id: int, followee_id: int, format: Optional[str] = None
    ) -> Response:
        """Create a following relationship where the follower starts following the followee."""
        follower = get_object_or_404(User, pk=follower_id)
        followee = get_object_or_404(User, pk=followee_id)

        if follower == followee:
            return Response(
                {"error": OWN_FOLLOW_ERROR}, status=status.HTTP_400_BAD_REQUEST
            )

        if follower.is_following(followee):
            return Response(
                {"error": ALREADY_FOLLOW},
                status=status.HTTP_400_BAD_REQUEST,
            )

        follower.follow(followee)
        return Response({"message": NEW_FOLLOW_MESSAGE}, status=status.HTTP_200_OK)


class UserListAPIView(APIView):
    """
    API view to list all users.
    Only accessible to authenticated users.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, format: Optional[str] = None) -> Response:
        """Retrieve and return a list of all users."""
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
