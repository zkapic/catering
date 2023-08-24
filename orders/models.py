from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    ORDER_TYPES = (
        (1, 'Type 1'),
        (2, 'Type 2'),
        # Add more types if needed
    )

    ORDER_STATUS = (
        (1, 'Pending'),
        (2, 'Completed'),
        # Add more status options if needed
    )

    city = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    date = models.DateTimeField()
    type = models.IntegerField(choices=ORDER_TYPES)
    status = models.IntegerField(choices=ORDER_STATUS)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order #{self.id} - {self.city}"