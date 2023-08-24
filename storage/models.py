from django.db import models
from django.contrib.auth.models import User

class Storage(models.Model):
    STORAGE_TYPES = (
        (1, 'Type 1'),
        (2, 'Type 2'),
        # Add more types if needed
    )

    STORAGE_STATUS = (
        (1, 'Active'),
        (2, 'Not active'),
        # Add more status options if needed
    )

    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=200)
    price = models.FloatField()
    type = models.IntegerField(choices=STORAGE_TYPES)
    status = models.IntegerField(choices=STORAGE_STATUS)

    def __str__(self):
        return f"Storage #{self.id} - {self.name}"