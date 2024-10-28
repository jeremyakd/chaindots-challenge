from comment.views import CommentListAPIView
from django.urls import path
from post.views import PostDetailAPIView, PostManagerAPIView

urlpatterns = [
    path("", PostManagerAPIView.as_view(), name="post-manager"),
    path("<int:id>/", PostDetailAPIView.as_view(), name="post-detail"),
    path("<int:id>/comments/", CommentListAPIView.as_view(), name="comments-by-post"),
]
