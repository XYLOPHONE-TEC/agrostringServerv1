from django.shortcuts import render

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import CartItem, Order, OrderItem
from farmers.models import Produce
from django.db import transaction
from django.utils.translation import gettext_lazy as _

class CartListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart_items = CartItem.objects.filter(user=request.user)
        data = []
        total_cost = 0
        for item in cart_items:
            item_total = item.quantity * float(item.produce.price_per_kg)
            total_cost += item_total
            data.append(
                {
                    "produce_id": item.produce.id,
                    "produce": str(item.produce),
                    "quantity": item.quantity,
                    "price_per_kg": float(item.produce.price_per_kg),
                    "item_total": item_total,
                }
            )
        return Response({"cart": data, "total_cost": total_cost})


class AddToCartView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        produce_id = request.data.get("produce_id")
        quantity = int(request.data.get("quantity", 1))
        produce = Produce.objects.get(id=produce_id, status="approved")
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user, produce=produce, defaults={"quantity": quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        return Response({"detail": "Added to cart."}, status=status.HTTP_200_OK)


class RemoveFromCartView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        produce_id = request.data.get("produce_id")
        CartItem.objects.filter(user=request.user, produce_id=produce_id).delete()
        return Response({"detail": "Removed from cart."}, status=status.HTTP_200_OK)


class CheckoutView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items.exists():
            return Response(
                {"detail": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST
            )
        total_cost = 0
        order = Order.objects.create(user=request.user, total_cost=0, is_paid=False)
        for item in cart_items:
            item_total = item.quantity * float(item.produce.price_per_kg)
            total_cost += item_total
            OrderItem.objects.create(
                order=order,
                produce=item.produce,
                quantity=item.quantity,
                price_per_kg=item.produce.price_per_kg,
            )
        order.total_cost = total_cost
        order.save()
        cart_items.delete()
        return Response(
            {"detail": "Order placed.", "order_id": order.id, "total_cost": total_cost},
            status=status.HTTP_201_CREATED,
        )
