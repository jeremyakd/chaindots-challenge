import pytest
from django.urls import reverse
from faker import Faker
from post.constants import COMMENTS_NUMBER, POST_ALEADY_EXIST_ERROR, TITLE_ERROR
from post.models import Post
from rest_framework import status
from tests.factories import CommentFactory, PostFactory
from user.models import User
from tests.conftest import user, client, auth_client


faker = Faker()


@pytest.mark.django_db
class TestPostAPI:
    """Class to test post endpoints"""

    @pytest.fixture(autouse=True)
    def setup(self, auth_client, user, client):
        """Setup fixture for initializing test variables."""
        self.user = user
        self.client = client
        self.auth_client = auth_client

    def generate_post_data(self, title=None, content=None):
        """Generate post data for tests."""
        return {
            "title": title or faker.sentence(nb_words=5),
            "content": content or faker.paragraph(nb_sentences=3),
            "author": self.user.id,
        }

    def test_create_post_success(self):
        """Test case for successfully creating a post."""
        post_data = self.generate_post_data()
        response = self.auth_client.post(
            reverse("post-manager"), post_data, format="json"
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert Post.objects.filter(title=post_data["title"]).exists()

    def test_create_post_unauthenticated(self):
        """Test case for creating a post without authentication."""
        post_data = self.generate_post_data()
        self.client.logout()
        response = self.client.post(reverse("post-manager"), post_data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_post_invalid_title(self):
        """Test case for creating a post with an invalid title."""
        post_data = self.generate_post_data(title="Short")
        response = self.auth_client.post(
            reverse("post-manager"), post_data, format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data
        assert TITLE_ERROR in response.data["error"]

    def test_create_post_duplicate_content(self):
        """Test case for preventing post creation with duplicate content."""
        content = faker.paragraph(nb_sentences=3)
        PostFactory.create(content=content)

        post_data = self.generate_post_data(content=content)
        response = self.auth_client.post(
            reverse("post-manager"), post_data, format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data
        assert POST_ALEADY_EXIST_ERROR in response.data["error"]

    def test_create_post_failed_by_author(self):
        author_id = User.objects.last().id + 1
        post_data = self.generate_post_data({"author": author_id})
        response = self.client.post(reverse("post-manager"), post_data, format="json")
        assert response, status.HTTP_400_BAD_REQUEST

    def test_get_post_details(self):
        """Test to retrieve a post's details, including comments and author."""
        self.post = PostFactory()
        for _ in range(5):
            CommentFactory(post=self.post)
        url = reverse("post-detail", kwargs={"id": self.post.id})
        response = self.auth_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert "post" in response.data
        assert "author" in response.data
        assert "recent_comments" in response.data
        assert len(response.data["recent_comments"]) == COMMENTS_NUMBER

    def test_get_non_existent_post(self):
        """Test to verify response for non-existent post."""
        url = reverse("post-detail", kwargs={"id": 99999})
        response = self.client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "error" in response.data
        assert response.data["error"] == "Post not found"
