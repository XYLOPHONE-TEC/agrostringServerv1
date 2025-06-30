from django.urls import path
from .views import (
    FarmerProduceListCreateView,
    FarmerProduceDetailView,
    # FarmerCarbonView
)
from .admin_actions import PublicProduceListView

urlpatterns = [
    path("produce/", FarmerProduceListCreateView.as_view(), name="produce-list"),
    path("produce/<int:pk>/", FarmerProduceDetailView.as_view(), name="produce-detail"),
    path(
        "public/produce/", PublicProduceListView.as_view(), name="public-produce-list"
    ),
    # path('carbon/', FarmerCarbonView.as_view(), name='carbon-tracker'),
]
