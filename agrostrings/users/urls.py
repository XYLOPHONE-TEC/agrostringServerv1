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
    UserDeleteView,
    UpdateMyProfileView
)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),

    path("me/", MeView.as_view()),

    path("dashboard/farmer/", FarmerDashboardView.as_view()),
    path("dashboard/buyer/", BuyerDashboardView.as_view()),
    path("dashboard/admin/", AdminDashboardView.as_view()),
    path("field-operator/farmers/", FieldOperatorFarmersView.as_view()),
    
    #viewing a list of all users including the super admin
    path('list/', UserListView.as_view(), name='user-list'),
    path('detail/<int:id>/', UserDetailView.as_view(), name='user-detail'),
    #viewing a list od admins without the super admin
    path('admins/', AdminListView.as_view(), name='admin-list'),

    path('delete/<int:id>/', UserDeleteView.as_view(), name='user-delete'),
    path('update/me/', UpdateMyProfileView.as_view(), name='user-update-self')


]
