import factory
from comment.models import Comment
from post.models import Post
from user.models import User


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for creating users"""

    class Meta:
        model = User

    email = factory.Faker("email")
    username = factory.Faker("user_name")
    password = factory.PostGenerationMethodCall("set_password", "defaultpassword")


class PostFactory(factory.django.DjangoModelFactory):
    """Factory for creating posts"""

    class Meta:
        model = Post

    author = factory.SubFactory(UserFactory)
    title = factory.Faker("sentence")
    content = factory.Faker("text")


class CommentFactory(factory.django.DjangoModelFactory):
    """Factory for creating comments"""

    class Meta:
        model = Comment

    author = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)
    content = factory.Faker("text")
