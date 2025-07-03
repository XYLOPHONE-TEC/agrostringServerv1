from django.urls import path
from .views import FarmerCarbonDataCreate, FarmerCarbonDataDetail

urlpatterns = [
    path('data/', FarmerCarbonDataCreate.as_view(), name='create-data'),
    path('data/<int:pk>/', FarmerCarbonDataDetail.as_view(), name='data-detail'),
]
