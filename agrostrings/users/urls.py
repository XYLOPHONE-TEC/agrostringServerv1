from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    MeView,
    FarmerDashboardView,
    BuyerDashboardView,
    AdminDashboardView,
    FieldOperatorFarmersView,
)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("me/", MeView.as_view()),
    path("dashboard/farmer/", FarmerDashboardView.as_view()),
    path("dashboard/buyer/", BuyerDashboardView.as_view()),
    path("dashboard/admin/", AdminDashboardView.as_view()),
    path("field-operator/farmers/", FieldOperatorFarmersView.as_view()),
]
