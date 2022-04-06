from django.db import models


class Foods(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    usual_measure = models.FloatField(default=0)
    hc_rations = models.FloatField(default=0)
    glycemic_index = models.IntegerField(default=0)

    class Meta:
        ordering = ['-id']
