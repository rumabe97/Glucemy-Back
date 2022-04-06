from django.db import models
from django.db.models.deletion import CASCADE

from foods.models import Foods
from users.models import User


class Records(models.Model):
    blood_glucose = models.FloatField(default=0)
    carbohydrates = models.FloatField(default=0)
    annotations = models.TextField(default="", max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    foods = models.ManyToManyField(Foods, related_name="records", related_query_name='record')
    user = models.ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='records',
        related_query_name='record'
    )

    class Meta:
        ordering = ['-id']
