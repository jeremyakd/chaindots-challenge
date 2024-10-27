from django.urls import path
from rest_framework import routers
from user.views import UserCreateFollowAPIView, UserDetailAPIView, UserListCreateAPIView

router = routers.DefaultRouter()


urlpatterns = [
    path("api/users/", UserListCreateAPIView.as_view(), name="user-list-create"),
    path("api/users/<int:user_id>/", UserDetailAPIView.as_view(), name="user-detail"),
    path(
        "api/users/<int:follower_id>/follow/<int:followee_id>/",
        UserCreateFollowAPIView.as_view(),
        name="create-follow",
    ),
]
