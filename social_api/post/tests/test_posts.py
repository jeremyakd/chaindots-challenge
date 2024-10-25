import pytest
from django.contrib.auth import get_user_model
from post.models import Post

User = get_user_model()


@pytest.mark.django_db
class TestPostModel:
    def test_create_post(self):
        author = User.objects.create_user(
            username="author", email="author@example.com", password="password123"
        )
        post = Post.objects.create(author=author, content="This is a test post.")

        assert post.author == author
        assert post.content == "This is a test post."
