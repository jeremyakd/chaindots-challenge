from django.urls import path
from post.views import PostManagerAPIView


urlpatterns = [
    path("api/posts/", PostManagerAPIView.as_view(), name="post-manager"),
]
