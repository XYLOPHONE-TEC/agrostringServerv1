import uuid
import secrets
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()
from django.utils.translation import gettext_lazy as _


class VideoCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Video(models.Model):
    CONTENT_TYPES = [
        ("tutorial", "Tutorial"),
        ("news", "News"),
        ("story", "Success Story"),
        ("experiment", "Experiment"),
    ]

    SEASONS = [
        ("dry", "Dry Season"),
        ("wet", "Wet Season"),
        ("harvest", "Harvest"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_file = models.FileField(upload_to="videos/")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(VideoCategory, related_name="videos")
    created_at = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(blank=True)
    views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, related_name="liked_videos", blank=True)

    # NEW FIELDS
    region = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=100, blank=True)
    sub_category = models.CharField(max_length=100, blank=True)
    content_type = models.CharField(
        max_length=50, choices=CONTENT_TYPES, default="tutorial"
    )
    season = models.CharField(max_length=50, choices=SEASONS, blank=True)
    device_type = models.CharField(max_length=50, blank=True)

    def like_count(self):
        return self.likes.count()

    def view(self):
        self.views += 1
        self.save()

    def engagement_score(self):
        # Example: 1 view = 1pt, 1 like = 3pts, 1 comment = 2pts
        return self.views + (self.likes.count() * 3) + (self.comments.count() * 2)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

from django.utils.translation import gettext_lazy as _
class AgroStringsTVSchedule(models.Model):
    STREAM_TYPE_CHOICES = [
        ("live", "Live"),
        ("pre_recorded", "Pre-Recorded"),
    ]
    title = models.CharField(max_length=255)
    stream_type = models.CharField(
        max_length=20, choices=STREAM_TYPE_CHOICES, default="pre_recorded"
    )
    video = models.FileField(
        upload_to="tv_videos/",
        blank=True,
        null=True,
        help_text="Upload a video for pre-recorded content.",
    )
    video_url = models.URLField(
        blank=True,
        null=True,
        help_text="YouTube/Vimeo link for pre-recorded content.",
    )
    category = models.ForeignKey(VideoCategory, on_delete=models.SET_NULL, null=True)
    start_time = models.DateTimeField(
        help_text="The time the live stream is scheduled to start.", default=timezone.now
    )
    end_time = models.DateTimeField(
        blank=True, null=True, help_text="The time the live stream is scheduled to end."
    )
    is_downloadable = models.BooleanField(default=False)
    language = models.CharField(
        max_length=30,
        choices=[
            ("en", _("English")),
            ("lg", _("Luganda")),
            ("sw", _("Swahili")),
        ],
        default="en",
        verbose_name=_("Language"),
    )
    is_live = models.BooleanField(
        default=False, help_text="Indicates if the stream is currently live."
    )
    stream_key = models.CharField(
        max_length=255,
        unique=True,
        blank=True,
        null=True,
        help_text="The unique key for the broadcaster to use.",
    )

    def save(self, *args, **kwargs):
        if self.stream_type == "live" and not self.stream_key:
            # Generate a unique and secure stream key
            self.stream_key = f"live_{secrets.token_urlsafe(16)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.get_stream_type_display()})"


class TVRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tv_video = models.ForeignKey(
        AgroStringsTVSchedule, on_delete=models.CASCADE, related_name="ratings"
    )
    rating = models.PositiveSmallIntegerField()  # 1-5 stars
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "tv_video")


class TVView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tv_video = models.ForeignKey(
        AgroStringsTVSchedule, on_delete=models.CASCADE, related_name="views"
    )
    watched_at = models.DateTimeField(auto_now_add=True)
