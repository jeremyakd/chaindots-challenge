from comment.models import Comment
from comment.serializer import CommentSerializer
from django.core.exceptions import ObjectDoesNotExist
from post.models import Post
from user.models import User


class CommentService:
    @staticmethod
    def get_user_and_post(author_id: int, post_id: int):
        try:
            user = User.objects.get(pk=author_id)
            post = Post.objects.get(pk=post_id)
            return user, post
        except ObjectDoesNotExist:
            raise AssertionError("User or Post not found")

    @staticmethod
    def create_comment(user: User, post: Post, content: str) -> Comment:
        comment = Comment(author=user, post=post, content=content)
        comment.save()
        return comment

    @staticmethod
    def get_comments_by_post(post) -> CommentSerializer:
        comments = post.post_comment_set.all()
        return CommentSerializer(comments, many=True)

    @staticmethod
    def validate_comment_data(data):
        author_id = data.get("author_id")
        comment_content = data.get("comment")

        if not author_id or not comment_content:
            raise ValueError("Missing author_id or comment.")
