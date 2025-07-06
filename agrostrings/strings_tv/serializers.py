# serializers.py
from rest_framework import serializers
from .models import Video, Comment, VideoCategory, AgroStringsTVSchedule

class VideoCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoCategory
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

class VideoSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    tags = VideoCategorySerializer(many=True, read_only=True)
    like_count = serializers.ReadOnlyField()

    class Meta:
        model = Video
        fields = '__all__'

class AgroStringsTVScheduleSerializer(serializers.ModelSerializer):
    category = VideoCategorySerializer(read_only=True)

    class Meta:
        model = AgroStringsTVSchedule
        fields = '__all__'
