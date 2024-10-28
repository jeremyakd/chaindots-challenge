from comment.serializer import CommentSerializer
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from post.constants import COMMENTS_NUMBER, POST_ALEADY_EXIST_ERROR, TITLE_ERROR
from post.models import Post
from post.serializer import PostSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from user.serializer import UserSerializer


class PostManagerAPIView(APIView):
    """
    View to handle creating and listing posts.
    """

    permission_classes = [IsAuthenticated]

    def get_posts(self, request):
        """Retrieve posts based on filters."""
        posts = Post.objects.all()
        if author_id := request.query_params.get("author_id"):
            posts = posts.filter(author_id=author_id)

        from_date = request.query_params.get("from_date")
        to_date = request.query_params.get("to_date")
        if from_date and to_date:
            posts = posts.filter(created_at__range=[from_date, to_date])

        return posts.order_by("-created_at")

    def paginate(self, request, posts):
        """Paginate the post list."""
        page_size = int(request.query_params.get("page_size", 20))
        page_number = int(request.query_params.get("page_number", 1))
        paginator = Paginator(posts, page_size)

        try:
            return paginator.page(page_number)
        except PageNotAnInteger:
            return paginator.page(1)
        except EmptyPage:
            return []

    def validate_post_data(self, data):
        """Validate title length and duplicate content."""
        title = data.get("title")
        if title and len(title) < 10:
            return False, {"error": TITLE_ERROR}

        content = data.get("content")
        if Post.objects.filter(content=content).exists():
            return False, {"error": POST_ALEADY_EXIST_ERROR}

        return True, {}

    def get(self, request, format=None):
        """Handle GET request for listing posts with filters and pagination."""
        posts = self.get_posts(request)
        paginated_posts = self.paginate(request, posts)
        serializer = PostSerializer(paginated_posts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """Handle POST request for creating a new post."""
        is_valid, errors = self.validate_post_data(request.data)
        if not is_valid:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id, format=None):
        try:
            post = Post.objects.get(pk=id)
            recent_comments = post.post_comment_set.all().order_by("-created_at")[
                :COMMENTS_NUMBER
            ]
            post_data = PostSerializer(post).data
            author_data = UserSerializer(post.author).data
            comments_data = CommentSerializer(recent_comments, many=True).data
            response_data = {
                "post": post_data,
                "author": author_data,
                "recent_comments": comments_data,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )
