# serializers.py
from rest_framework import serializers
from .models import Video, Comment, VideoCategory, AgroStringsTVSchedule


class VideoCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoCategory
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"


class VideoSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    tags = VideoCategorySerializer(many=True, read_only=True)
    like_count = serializers.ReadOnlyField()
    engagement_score = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = "__all__"

    def get_engagement_score(self, obj):
        return obj.engagement_score()

    def to_internal_value(self, data):
        # Accept both value and display name for 'season' and 'content_type'
        season_map = {display: value for value, display in Video.SEASONS}
        content_type_map = {display: value for value, display in Video.CONTENT_TYPES}
        # Accept display name for season
        season = data.get("season")
        if season:
            # Accept both value and display name
            if season in season_map:
                data["season"] = season_map[season]
        # Accept display name for content_type
        content_type = data.get("content_type")
        if content_type:
            if content_type in content_type_map:
                data["content_type"] = content_type_map[content_type]
        return super().to_internal_value(data)


class AgroStringsTVScheduleSerializer(serializers.ModelSerializer):
    category = VideoCategorySerializer(read_only=True)

    class Meta:
        model = AgroStringsTVSchedule
        fields = '__all__'

    def validate(self, data):
        if not data.get('video') and not data.get('video_url'):
            raise serializers.ValidationError("Either video file or video URL is required.")
        return data
