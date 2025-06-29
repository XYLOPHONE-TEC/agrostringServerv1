from django.urls import path
from .views import (
    FarmerProduceListCreateView,
    FarmerProduceDetailView,
    #FarmerCarbonView
)

urlpatterns = [
    path('produce/', FarmerProduceListCreateView.as_view(), name='produce-list'),
    path('produce/<int:pk>/', FarmerProduceDetailView.as_view(), name='produce-detail'),
    #path('carbon/', FarmerCarbonView.as_view(), name='carbon-tracker'),
]
