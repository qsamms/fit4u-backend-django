from django.db import models
from api.models import ExternalExercise, CustomUser


class WorkoutPlan(models.Model):
    class Meta:
        app_label = "api"

    name = models.CharField(null=False, blank=False, max_length=255, default="")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    exercises = models.ManyToManyField(ExternalExercise)
