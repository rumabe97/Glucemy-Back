from django.db import models
from django.db.models.deletion import CASCADE

from foods.models import Foods
from phasesDay.models import PhasesDay
from users.models import User


class Favourites(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='favourites',
        related_query_name='favourite'
    )
    foods = models.ManyToManyField(Foods, related_name="favourites", related_query_name='favourite')
    phasesDay = models.ManyToManyField(PhasesDay, related_name="favourites", related_query_name='favourite')

    class Meta:
        ordering = ['-id']
