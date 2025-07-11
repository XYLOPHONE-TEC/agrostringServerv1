from django.db import models
from django.conf import settings
from farmers.models import Produce
from django.utils.translation import gettext_lazy as _

class CartItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart_items"
    )
    produce = models.ForeignKey(Produce, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "produce")


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2)
    is_paid = models.BooleanField(default=False)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    produce = models.ForeignKey(Produce, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_per_kg = models.DecimalField(max_digits=8, decimal_places=2)
