from django.urls import path
from rest_framework import routers
from user.views import (
    UserCreateAPIView,
    UserCreateFollowAPIView,
    UserDetailAPIView,
    UserListAPIView,
)

router = routers.DefaultRouter()


urlpatterns = [
    path("api/users/", UserListAPIView.as_view(), name="users-list"),
    path("api/users/create/", UserCreateAPIView.as_view(), name="user-create"),
    path("api/users/<int:user_id>/", UserDetailAPIView.as_view(), name="user-detail"),
    path(
        "api/users/<int:follower_id>/follow/<int:followee_id>/",
        UserCreateFollowAPIView.as_view(),
        name="create-follow",
    ),
]
