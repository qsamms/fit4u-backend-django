from django.db import models
from .custom_user import CustomUser


class Workout(models.Model):
    class Meta:
        app_label = "api"

    datetime = models.DateTimeField(null=False, blank=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(null=False, blank=False, max_length=150, default="")
