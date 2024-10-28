import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from tests.factories import CommentFactory, PostFactory, UserFactory


@pytest.fixture
def user():
    """Fixture that returns a user."""
    return UserFactory.create()


@pytest.fixture
def post(user):
    """Fixture that returns a post."""
    return PostFactory(author=user)


@pytest.fixture
def comment(post, user):
    """Fixture that returns a comment."""
    return CommentFactory(post=post, author=user)


@pytest.fixture
def client():
    """Fixture that returns a client."""
    return APIClient()


@pytest.fixture
def auth_client(client, user):
    """Fixture that returns an authenticated client."""
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return client
