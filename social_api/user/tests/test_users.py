import pytest
from django.urls import reverse
from rest_framework import status
from tests.conftest import user, post, comment, client, auth_client
from tests.factories import UserFactory
from user.models import User


@pytest.mark.django_db
class TestUserAPI:
    """Class to test user endpoints"""

    @pytest.fixture(autouse=True)
    def setup(self, auth_client, post, client, user):
        """Setup fixture for initializing test variables."""
        self.user = user
        self.post = post
        self.client = client
        self.auth_client = auth_client

    def test_create_user(self):
        """Test case for creating a new user."""
        user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword123",
        }
        response = self.auth_client.post(
            reverse("user-list-create"), user_data, format="json"
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(username="newuser").exists()

    def test_follow_user_success(self):
        """Test case for successfully following a user."""
        follower = self.user
        followee = UserFactory.create()

        response = self.auth_client.post(
            reverse(
                "create-follow",
                kwargs={"follower_id": follower.id, "followee_id": followee.id},
            ),
            data={},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert "You are now following this user" in response.data["message"]
        assert followee.is_followed_by(follower)

    def test_follow_user_fail_self_follow(self):
        """Test case for preventing a user from following themselves."""
        user = self.user

        response = self.auth_client.post(
            reverse(
                "create-follow", kwargs={"follower_id": user.id, "followee_id": user.id}
            ),
            data={},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "You cannot follow yourself." in response.data["error"]

    def test_retrieve_user(self):
        """Test case for retrieving a user's details."""
        response = self.auth_client.get(
            reverse("user-detail", kwargs={"user_id": self.user.id})
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == self.user.username
        assert response.data["email"] == self.user.email

    def test_retrieve_non_existent_user(self):
        """Test case for retrieving a non-existent user's details."""
        response = self.auth_client.get(reverse("user-detail", kwargs={"user_id": 999}))
        assert response.status_code == status.HTTP_404_NOT_FOUND
