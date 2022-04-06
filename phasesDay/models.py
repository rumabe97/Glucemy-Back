from django.db import models


class PhasesDay(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']
