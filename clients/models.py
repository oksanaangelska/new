from django.db import models


class Client(models.Model):
    telegram_id = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=256)
    telegram_username = models.CharField(max_length=256, null=True, blank=True)
