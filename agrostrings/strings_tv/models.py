from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()



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
    video_file = models.FileField(upload_to='videos/')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(VideoCategory, related_name='videos')
    created_at = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(blank=True)
    views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='liked_videos', blank=True)

    # NEW FIELDS
    region = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=100, blank=True)
    sub_category = models.CharField(max_length=100, blank=True)
    content_type = models.CharField(max_length=50, choices=CONTENT_TYPES, default="tutorial")
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
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class AgroStringsTVSchedule(models.Model):
    title = models.CharField(max_length=255)
    video = models.FileField(upload_to='tv_videos/')
    category = models.ForeignKey(VideoCategory, on_delete=models.SET_NULL, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_downloadable = models.BooleanField(default=False)
