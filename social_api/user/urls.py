from django.urls import path
from rest_framework import routers
from user.views import UserCreateFollowAPIView, UserDetailAPIView, UserListCreateAPIView

router = routers.DefaultRouter()


urlpatterns = [
    path("", UserListCreateAPIView.as_view(), name="user-list-create"),
    path("<int:user_id>/", UserDetailAPIView.as_view(), name="user-detail"),
    path(
        "<int:follower_id>/follow/<int:followee_id>/",
        UserCreateFollowAPIView.as_view(),
        name="create-follow",
    ),
]
