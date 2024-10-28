import pytest
from comment.models import Comment
from rest_framework import status
from rest_framework.reverse import reverse
from tests.conftest import user, client, auth_client, post, comment


@pytest.mark.django_db
class TestCommentListAPIView:
    """Tests for the Comment List API view."""

    @pytest.fixture(autouse=True)
    def setup(self, user, auth_client, post, comment):
        """Set up the required objects for each test."""
        self.user = user
        self.post = post
        self.auth_client = auth_client

    def test_get_post_comments(self):
        """Test that fetching comments by post ID returns correct data."""
        url = reverse("comments-by-post", kwargs={"id": self.post.id})
        response = self.auth_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert "comments" in response.data
        assert len(response.data["comments"]) == 1

    def test_create_comment(self):
        """Test creating a new comment for a post."""
        url = reverse("comments-by-post", kwargs={"id": self.post.id})
        data = {"author_id": self.user.id, "comment": "New comment"}
        response = self.auth_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Comment.objects.count() == 2
        assert Comment.objects.last().content == "New comment"

    def test_create_comment_invalid(self):
        """Test creating a comment with invalid data (e.g., empty content)."""
        url = reverse("comments-by-post", kwargs={"id": self.post.id})
        data = {"author_id": self.user.id, "comment": ""}
        response = self.auth_client.post(url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data
