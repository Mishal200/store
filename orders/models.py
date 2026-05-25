from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=20, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    def save(self, *args, **kwargs):
        # Generate order number automatically
        if not self.order_number:
            last_id = Order.objects.count() + 1
            self.order_number = f"ORD{1000 + last_id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_number} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"