from django.urls import path

from .views import CartListView, AddToCartView, RemoveFromCartView, CheckoutView

urlpatterns = [
    # path(
    #     "public/produce/", PublicProduceListView.as_view(), name="public-produce-list"
    # ),
    path("cart/", CartListView.as_view(), name="cart-list"),
    path("cart/add/", AddToCartView.as_view(), name="cart-add"),
    path("cart/remove/", RemoveFromCartView.as_view(), name="cart-remove"),
    path("cart/checkout/", CheckoutView.as_view(), name="cart-checkout"),
]
