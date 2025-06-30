from django.urls import path

from .views import ProduceApproveRejectView

urlpatterns = [
    path(
        "produce/<int:pk>/approve-reject/",
        ProduceApproveRejectView.as_view(),
        name="produce-approve-reject",
    ),
]
