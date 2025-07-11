from django.shortcuts import render

from rest_framework import viewsets, permissions
from .models import Video, Comment, VideoCategory, AgroStringsTVSchedule, TVRating, TVView
from .serializers import (
    VideoSerializer,
    CommentSerializer,
    VideoCategorySerializer,
    AgroStringsTVScheduleSerializer,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .recommendation import recommend_videos_for_user
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
import re
from .models import VideoCategory
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

# Common English stopwords to ignore (you can expand this list)
STOP_WORDS = {
    "i",
    "my",
    "this",
    "the",
    "a",
    "an",
    "and",
    "or",
    "is",
    "in",
    "on",
    "of",
    "to",
    "with",
    "was",
    "for",
    "at",
    "by",
    "from",
    "used",
    "it",
}


class VideoViewSet(viewsets.ModelViewSet):
    queryset = (
        Video.objects.select_related()
        .prefetch_related("tags", "likes", "comments")
        .order_by("-created_at")
    )

    # queryset = Video.objects.all().order_by('-created_at')
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["region", "category", "sub_category", "season", "content_type"]
    search_fields = ["title", "description"]

    def perform_create(self, serializer):
        video = serializer.save(user=self.request.user)

        # Use only the title for tag extraction
        title_text = video.title.lower()

        # Extract individual words from the title
        keywords = re.findall(r"\b\w+\b", title_text)

        # Remove common/meaningless words
        filtered_keywords = [word for word in keywords if word not in STOP_WORDS]

        # Create or reuse tags and link them to the video
        for word in filtered_keywords:
            tag, created = VideoCategory.objects.get_or_create(
                name__iexact=word, defaults={"name": word}
            )
            video.tags.add(tag)

        video.save()

    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        video = self.get_object()
        video.likes.add(request.user)
        return Response({"status": "liked"})

    @action(detail=True, methods=["post"])
    def view(self, request, pk=None):
        video = self.get_object()
        video.view()
        return Response({"status": "view counted"})

    @action(detail=False, methods=["get"])
    def trending(self, request):
        videos = Video.objects.all()
        videos = sorted(videos, key=lambda v: v.engagement_score(), reverse=True)[:10]
        serializer = self.get_serializer(videos, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class VideoCategoryViewSet(viewsets.ModelViewSet):
    queryset = VideoCategory.objects.all()
    serializer_class = VideoCategorySerializer

    def get_permissions(self):
        # Only allow admin/superadmin to create, update, or delete
        if self.action in ["create", "update", "partial_update", "destroy"]:
            from users.permissions import IsAdmin, IsSuperAdmin

            return [(IsAdmin | IsSuperAdmin)()]
        # Allow any user to list or retrieve
        return [permissions.AllowAny()]


class RecommendedVideosView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        videos = recommend_videos_for_user(request.user)
        serializer = VideoSerializer(videos, many=True, context={"request": request})
        return Response(serializer.data)


class AgroStringsTVScheduleViewSet(viewsets.ModelViewSet):
    queryset = AgroStringsTVSchedule.objects.all()
    serializer_class = AgroStringsTVScheduleSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            from users.permissions import IsAdmin, IsSuperAdmin
            return [(IsAdmin | IsSuperAdmin)()]
        return [permissions.AllowAny()]

    
    @action(detail=True, methods=['post'])
    def rate(self, request, pk=None):
        tv_video = self.get_object()
        rating_value = request.data.get('rating')
        if not rating_value or not (1 <= int(rating_value) <= 5):
            return Response({'detail': 'Rating must be 1-5.'}, status=status.HTTP_400_BAD_REQUEST)
        rating, created = TVRating.objects.update_or_create(
            user=request.user, tv_video=tv_video, defaults={'rating': rating_value}
        )
        return Response({'detail': 'Rating submitted.'})
    
    @action(detail=True, methods=['post'], permission_classes=[AllowAny])
    def watch(self, request, pk=None):
        tv_video = self.get_object()

        if request.user.is_authenticated:
        # Logged-in user
            TVView.objects.create(user=request.user, tv_video=tv_video)
        else:
        # Anonymous users — optionally just log to console or ignore
            print(f"Anonymous user watched TV ID {tv_video.id} at {now()}")
        # Optional: You could also log to a file or use a custom AnonymousView model

        return Response({'detail': 'View recorded.'})

