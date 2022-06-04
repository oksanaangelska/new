from django.db import models

from clients.models import Client


class Order(models.Model):
    CAKE = 'cake'
    SWEETS = 'sweets'
    BAKE = 'bake'

    TYPE_CHOICES = (
        [CAKE, 'Cake'],
        [SWEETS, 'Sweets'],
        [BAKE, 'Bake'],
    )

    url = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    is_sent = models.BooleanField(default=False)
