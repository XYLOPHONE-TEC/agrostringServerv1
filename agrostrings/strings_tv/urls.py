from django.urls import path
from .views import (
    VideoViewSet,
    CommentViewSet,
    VideoCategoryViewSet,
    AgroStringsTVScheduleViewSet,
    RecommendedVideosView,
)
from .webhooks import StreamOnPublishView, StreamOnPublishDoneView

# VIDEO paths
video_list = VideoViewSet.as_view({"get": "list", "post": "create"})
video_detail = VideoViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)
video_like = VideoViewSet.as_view({"post": "like"})
video_view = VideoViewSet.as_view({"post": "view"})
video_trending = VideoViewSet.as_view({"get": "trending"})

# COMMENT paths
comment_list = CommentViewSet.as_view({"get": "list", "post": "create"})
comment_detail = CommentViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)

# CATEGORY paths
category_list = VideoCategoryViewSet.as_view({"get": "list", "post": "create"})
category_detail = VideoCategoryViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)

# AGROSTRINGS TV paths
tv_list = AgroStringsTVScheduleViewSet.as_view({"get": "list", "post": "create"})
tv_detail = AgroStringsTVScheduleViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)
tv_rate = AgroStringsTVScheduleViewSet.as_view({"post": "rate"})
tv_watch = AgroStringsTVScheduleViewSet.as_view({"post": "watch"})

# ROUTES
urlpatterns = [
    # VIDEO
    path("videos/", video_list, name="video-list"),
    path("videos/<int:pk>/", video_detail, name="video-detail"),
    path("videos/<int:pk>/like/", video_like, name="video-like"),
    path("videos/<int:pk>/view/", video_view, name="video-view"),
    path(
        "videos/recommended/", RecommendedVideosView.as_view(), name="video-recommended"
    ),
    path("videos/trending/", video_trending, name="video-trending"),
    # COMMENT
    path("comments/", comment_list, name="comment-list"),
    path("comments/<int:pk>/", comment_detail, name="comment-detail"),
    # CATEGORY
    path("categories/", category_list, name="category-list"),
    path("categories/<int:pk>/", category_detail, name="category-detail"),
    # AGROSTRINGS TV
    path("television/", tv_list, name="tv-list"),
    path("television/<int:pk>/", tv_detail, name="tv-detail"),
    path("television/<int:pk>/rate/", tv_rate, name="tv-rate"),
    path("television/<int:pk>/watch/", tv_watch, name="tv-watch"),
    # WEBHOOKS
    path(
        "webhooks/stream/on_publish/",
        StreamOnPublishView.as_view(),
        name="webhook-stream-on-publish",
    ),
    path(
        "webhooks/stream/on_publish_done/",
        StreamOnPublishDoneView.as_view(),
        name="webhook-stream-on-publish-done",
    ),
]
