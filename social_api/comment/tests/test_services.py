import pytest
from comment.services import CommentService
from tests.conftest import user, post


@pytest.mark.django_db
class TestCommentService:
    @pytest.fixture(autouse=True)
    def setup(self, user, post):
        self.user = user
        self.post = post

    def test_get_user_and_post(self):
        user, post = CommentService.get_user_and_post(self.user.id, self.post.id)
        assert user == self.user
        assert post == self.post

    def test_create_comment(self):
        comment_content = "This is a test comment."
        comment = CommentService.create_comment(self.user, self.post, comment_content)
        assert comment.author == self.user
        assert comment.post == self.post
        assert comment.content == comment_content

    def test_get_comments_by_post(self):
        CommentService.create_comment(self.user, self.post, "First comment")
        CommentService.create_comment(self.user, self.post, "Second comment")
        comments = CommentService.get_comments_by_post(self.post)

        assert len(comments.data) == 2
        assert comments.data[0]["content"] == "First comment"
        assert comments.data[1]["content"] == "Second comment"
