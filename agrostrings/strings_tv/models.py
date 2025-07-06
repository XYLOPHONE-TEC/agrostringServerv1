from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class VideoCategory(models.Model):
    name = models.CharField(max_length=100)

class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_file = models.FileField(upload_to='videos/')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(VideoCategory, related_name='videos')
    created_at = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='liked_videos', blank=True)

    def like_count(self):
        return self.likes.count()

    def view(self):
        self.views += 1
        self.save()

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
