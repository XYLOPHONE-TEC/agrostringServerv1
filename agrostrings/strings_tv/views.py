from django.shortcuts import render

from rest_framework import viewsets, permissions
from .models import Video, Comment, VideoCategory, AgroStringsTVSchedule
from .serializers import VideoSerializer, CommentSerializer, VideoCategorySerializer, AgroStringsTVScheduleSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .recommendation import recommend_videos_for_user
from rest_framework.permissions import IsAuthenticated



import re
from .models import VideoCategory

# Common English stopwords to ignore (you can expand this list)
STOP_WORDS = {
    "i", "my", "this", "the", "a", "an", "and", "or", "is", "in", "on",
    "of", "to", "with", "was", "for", "at", "by", "from", "used", "it"
}

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all().order_by('-created_at')
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        video = serializer.save(user=self.request.user)

        # Use only the title for tag extraction
        title_text = video.title.lower()

        # Extract individual words from the title
        keywords = re.findall(r'\b\w+\b', title_text)

        # Remove common/meaningless words
        filtered_keywords = [word for word in keywords if word not in STOP_WORDS]

        # Create or reuse tags and link them to the video
        for word in filtered_keywords:
            tag, created = VideoCategory.objects.get_or_create(
                name__iexact=word,
                defaults={"name": word}
            )
            video.tags.add(tag)

        video.save()



    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        video = self.get_object()
        video.likes.add(request.user)
        return Response({'status': 'liked'})

    @action(detail=True, methods=['post'])
    def view(self, request, pk=None):
        video = self.get_object()
        video.view()
        return Response({'status': 'view counted'})



class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class VideoCategoryViewSet(viewsets.ModelViewSet):
    queryset = VideoCategory.objects.all()
    serializer_class = VideoCategorySerializer



class RecommendedVideosView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        videos = recommend_videos_for_user(request.user)
        serializer = VideoSerializer(videos, many=True, context={"request": request})
        return Response(serializer.data)



class AgroStringsTVScheduleViewSet(viewsets.ModelViewSet):
    queryset = AgroStringsTVSchedule.objects.all()
    serializer_class = AgroStringsTVScheduleSerializer
