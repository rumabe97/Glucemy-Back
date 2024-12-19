from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models.deletion import CASCADE

from foods.models import Foods
from phasesDay.models import PhasesDay
from users.models import User


class Records(models.Model):
    blood_glucose = models.FloatField(default=0)
    carbohydrates = ArrayField(
        models.FloatField(),
        default=list,
    )
    annotations = models.TextField(default="", max_length=255)
    hc_rations = models.FloatField(default=0)
    bolus = models.FloatField(default=0)
    units = models.FloatField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    foods = models.ManyToManyField(Foods, related_name="records", related_query_name='record')
    phasesDay = models.ForeignKey(PhasesDay, on_delete=CASCADE, related_name="records", related_query_name='record',
                                  null=False, blank=False)
    user = models.ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='records',
        related_query_name='record',
    )

    class Meta:
        ordering = ['-id']
