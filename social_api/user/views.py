from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import User
from user.serializer import UserSerializer


class UserCreateAPIView(APIView):
    """
    View to create a new user.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        """Creates a new user profile with provided data."""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPIView(APIView):
    """
    View for retrieving user data
    """

    permission_classes = [IsAuthenticated]

    def get_user_data(self, user: User) -> dict:
        """Method to retrieve and format user data"""
        serializer = UserSerializer(user)
        user_data = serializer.data
        user_data["total_posts"] = user.post_set.count()
        user_data["total_comments"] = user.comment_set.count()
        user_data["followers"] = UserSerializer(user.followers.all(), many=True).data
        user_data["following"] = UserSerializer(user.following.all(), many=True).data
        return user_data

    def get(self, request, user_id, format=None):
        """Method to retrieve user profile data by user ID."""
        user = get_object_or_404(User, pk=user_id)
        user_data = self.get_user_data(user)
        return Response(user_data)


class UserCreateFollowAPIView(APIView):
    """
    View for creating a new follow relationship
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, follower_id, followee_id, format=None):
        """Create a new follow relationship"""
        follower = get_object_or_404(User, pk=follower_id)
        followee = get_object_or_404(User, pk=followee_id)

        if follower == followee:
            return Response(
                {"error": "Cannot follow yourself"}, status=status.HTTP_400_BAD_REQUEST
            )

        if follower.is_following(followee):
            return Response(
                {"error": "Already following this user"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        follower.follow(followee)
        return Response({"message": "You are now following this user"})


class UserListAPIView(APIView):
    """
    View for list all users.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """Method to list all users"""
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
