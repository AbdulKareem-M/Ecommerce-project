from django.db import models
from user_application.models import User
from product.models import Product

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Allow multiple orders per user
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=100, 
        choices=[('pending', 'Pending'), ('completed', 'Completed'), ('cancelled', 'Cancelled')],
        default='pending'
    )

    def __str__(self):
        return f"Order {self.id} - {self.user.username} ({self.status})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", default=1)  # Changed order_id → order
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.item.name} (Order {self.order.id})"

class OrderSummary(models.Model):
    order_item_id = models.ForeignKey(OrderItem, on_delete=models.CASCADE, null=True, blank=True)
    order_id = models.CharField(max_length=200)
    payment_status = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=200, null=True, blank=True)
    total = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    