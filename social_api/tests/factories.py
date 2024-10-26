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

    content = factory.Faker("text")
    author = factory.SubFactory(UserFactory)  # Cambia `user` a `author`


class CommentFactory(factory.django.DjangoModelFactory):
    """Factory for creating comments"""

    class Meta:
        model = Comment

    content = factory.Faker("text")
    post = factory.SubFactory(PostFactory)
    user = factory.SubFactory(UserFactory)
