from django.db import models
from django.db.models.deletion import CASCADE

from users.models import User


class Records(models.Model):
    blood_glucose = models.FloatField(default=0)
    carbohydrates = models.FloatField(default=0)
    annotations = models.TextField(default="", max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='records',
        related_query_name='records'
    )

    class Meta:
        ordering = ['-id']
