from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    MeView,
    FarmerDashboardView,
    BuyerDashboardView,
    AdminDashboardView,
    FieldOperatorFarmersView,
    AdminListView,
    UserListView,
    UserDetailView,

    # UserUpdateView, UserDeleteView,
)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),

    path("me/", MeView.as_view()),

    path("dashboard/farmer/", FarmerDashboardView.as_view()),
    path("dashboard/buyer/", BuyerDashboardView.as_view()),
    path("dashboard/admin/", AdminDashboardView.as_view()),
    path("field-operator/farmers/", FieldOperatorFarmersView.as_view()),

    path('users/list/', UserListView.as_view(), name='user-list'),
    path('users/detail/<int:id>/', UserDetailView.as_view(), name='user-detail'),
    path('users/admins/', AdminListView.as_view(), name='admin-list'),

    # path('users/update/<int:id>/', UserUpdateView.as_view(), name='user-update'),
    # path('users/delete/<int:id>/', UserDeleteView.as_view(), name='user-delete'),


]
