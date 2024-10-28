from comment.services import CommentService
from post.models import Post
from post.serializer import PostSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class CommentListAPIView(APIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, id, format=None):
        try:
            post = Post.objects.get(pk=id)
            comments = CommentService.get_comments_by_post(post)
            post_serializer = PostSerializer(post)

            response_data = post_serializer.data
            response_data["comments"] = comments.data

            return Response(response_data)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request, id, format=None):
        data = request.data

        try:
            CommentService.validate_comment_data(data)  # Validación
            user, post = CommentService.get_user_and_post(data["author_id"], id)
            comment = CommentService.create_comment(user, post, data["comment"])

            return Response(
                {"comment": comment.content}, status=status.HTTP_201_CREATED
            )
        except AssertionError as error:
            return Response({"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as error:
            return Response({"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)
