# serializers.py
from rest_framework import serializers
from .models import (
    Video,
    Comment,
    VideoCategory,
    AgroStringsTVSchedule,
    TVRating,
    TVView,
)
from django.utils.translation import gettext_lazy as _


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
    average_rating = serializers.SerializerMethodField()
    view_count = serializers.SerializerMethodField()
    live_stream_url = serializers.SerializerMethodField()

    class Meta:
        model = AgroStringsTVSchedule
        fields = "__all__"
        read_only_fields = ("stream_key",)
        extra_fields = ["average_rating", "view_count", "live_stream_url"]

    def validate(self, data):
        stream_type = data.get("stream_type")
        if stream_type == "pre_recorded":
            if not data.get("video") and not data.get("video_url"):
                raise serializers.ValidationError(
                    "For pre-recorded streams, either a video file or a video URL is required."
                )
        return data

    def get_live_stream_url(self, obj):
        if obj.stream_type == "live" and obj.is_live:
            # This URL should point to your Nginx-RTMP HLS stream
            # The exact URL will depend on your Nginx configuration
            return f"http://your-media-server.com/hls/{obj.stream_key}.m3u8"
        return None

    def get_average_rating(self, obj):
        ratings = obj.ratings.all()
        if ratings.exists():
            return round(sum(r.rating for r in ratings) / ratings.count(), 2)
        return None

    def get_view_count(self, obj):
        return obj.views.count()


class TVRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TVRating
        fields = ["id", "user", "tv_video", "rating", "created_at"]
        read_only_fields = ["user", "created_at"]


class TVViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = TVView
        fields = ["id", "user", "tv_video", "watched_at"]
        read_only_fields = ["user", "watched_at"]
