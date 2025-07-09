# from .models import Video

# def recommend_videos_for_user(user):
#     liked_videos = user.liked_videos.all()

#     if not liked_videos.exists():
#         # Return trending if user has no likes
#         return Video.objects.all().order_by('-views')[:10]
    
#     categories = set(tag for video in liked_videos for tag in video.tags.all())
#     recommended = Video.objects.filter(tags__in=categories).exclude(likes=user).distinct().order_by('-views')[:10]

#      # Sort by engagement score
#     recommended = sorted(recommended, key=lambda v: v.engagement_score(), reverse=True)
#     return recommended



from .models import Video

def recommend_videos_for_user(user):
    liked_videos = user.liked_videos.all()

    if not liked_videos.exists():
        # If user has no likes yet, fallback to trending
        return Video.objects.all().order_by('-views')[:10]

    # Gather tags from videos the user liked
    categories = set(tag for video in liked_videos for tag in video.tags.all())

    # Get all videos with those tags (including already liked ones)
    recommended = Video.objects.filter(tags__in=categories).distinct()

    # Sort by engagement score (views + likes + comments)
    recommended = sorted(recommended, key=lambda v: v.engagement_score(), reverse=True)

    return recommended[:10]


