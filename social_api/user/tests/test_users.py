import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from user.models import User


@pytest.mark.django_db
class TestUserAPI:
    """Class to test user endpoint"""

    @pytest.fixture
    def client(self):
        """Fixture that return a client"""
        return APIClient()

    @pytest.fixture
    def create_user(self):
        """Fixture that creates a user"""
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )
        return user

    @pytest.fixture
    def auth_client(self, client, create_user):
        """Fixture that returns an authenticated client"""
        refresh = RefreshToken.for_user(create_user)
        access_token = str(refresh.access_token)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        return client

    def test_create_user(self, auth_client):
        """Create a new user test"""
        user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword123",
        }
        response = auth_client.post(reverse("user-create"), user_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(username="newuser").exists()

    def test_follow_user_success(self, auth_client):
        """
        Test the successful following of one user by another.
        """
        user_1 = User.objects.first()
        user_2 = User.objects.last()
        user_2.unfollow(
            user_1
        )  # Asegúrate de que el segundo usuario no siga al primero antes de probar

        response = auth_client.post(
            reverse(
                "create-follow",
                kwargs={"follower_id": user_2.id, "followee_id": user_1.id},
            ),
            data={},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert "You are now following this user" in response.data["message"]
        assert user_1.is_followed_by(user_2)

    def test_follow_user_fail_self_follow(self, auth_client):
        """
        Test that a user cannot follow themselves.
        """
        user = User.objects.last()

        response = auth_client.post(
            reverse(
                "create-follow", kwargs={"follower_id": user.id, "followee_id": user.id}
            ),
            data={},
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Cannot follow yourself" in response.data["error"]

    def test_retrieve_user(self, auth_client):
        """
        Test the retrieval of a user's details.
        """
        user = User.objects.last()
        response = auth_client.get(reverse("user-detail", kwargs={"user_id": user.id}))
        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == user.username
        assert response.data["email"] == user.email

    def test_retrieve_non_existent_user(self, auth_client):
        """
        Test the retrieval of a non-existent user's details.
        """
        response = auth_client.get(reverse("user-detail", kwargs={"user_id": 999}))
        assert response.status_code == status.HTTP_404_NOT_FOUND
