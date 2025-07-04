from django.urls import path
from .views import (
    FarmerProduceListCreateView,
    FarmerProduceDetailView,
    FarmerCommunityQuestionListCreateView,
    CommunityReplyCreateView,
    FarmInputRequestListCreateView,
    AdminReplyToRequestCreateView,
    AdminViewAllFarmInputRequests,
    CommunityRepliesByQuestionView,
    AdminRepliesByRequestView,

)
from .admin_actions import PublicProduceListView

urlpatterns = [
    path("produce/", FarmerProduceListCreateView.as_view(), name="produce-list"),
    path("produce/<int:pk>/", FarmerProduceDetailView.as_view(), name="produce-detail"),
    path(
        "public/produce/", PublicProduceListView.as_view(), name="public-produce-list"
    ),
    # Community Questions (Public Forum)
    path("community/questions/", FarmerCommunityQuestionListCreateView.as_view(), name="community-questions"),
    path("community/replies/", CommunityReplyCreateView.as_view(), name="community-replies"),
    path("community/replies/filter/", CommunityRepliesByQuestionView.as_view(), name="replies-by-question"),

    # Tool/Input Requests (Private)
    path("requests/my/", FarmInputRequestListCreateView.as_view(), name="my-tool-requests"),
    path("requests/all/", AdminViewAllFarmInputRequests.as_view(), name="all-tool-requests"),
    path("requests/reply/", AdminReplyToRequestCreateView.as_view(), name="admin-reply-request"),
    path("requests/replies/filter/", AdminRepliesByRequestView.as_view(), name="admin-replies-by-request"),


]
