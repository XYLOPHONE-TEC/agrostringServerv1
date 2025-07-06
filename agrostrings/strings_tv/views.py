from django.shortcuts import render

from rest_framework import viewsets, permissions
from .models import Video, Comment, VideoCategory, AgroStringsTVSchedule
from .serializers import VideoSerializer, CommentSerializer, VideoCategorySerializer, AgroStringsTVScheduleSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

from .recommendation import recommend_videos_for_user

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all().order_by('-created_at')
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

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



@action(detail=False, methods=['get'])
def recommended(self, request):
    videos = recommend_videos_for_user(request.user)
    serializer = self.get_serializer(videos, many=True)
    return Response(serializer.data)



class AgroStringsTVScheduleViewSet(viewsets.ModelViewSet):
    queryset = AgroStringsTVSchedule.objects.all()
    serializer_class = AgroStringsTVScheduleSerializer
