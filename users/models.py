from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    weight = models.FloatField(default=0)
    height = models.FloatField(default=0)
    age = models.IntegerField(default=0)
    profile_image = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-id']
