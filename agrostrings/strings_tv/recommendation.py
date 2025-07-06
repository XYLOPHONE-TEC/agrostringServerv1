from .models import Video

def recommend_videos_for_user(user):
    liked_videos = user.liked_videos.all()
    categories = set(tag for video in liked_videos for tag in video.tags.all())
    recommended = Video.objects.filter(tags__in=categories).exclude(likes=user).distinct().order_by('-views')[:10]
    return recommended
