from django.db import models
from api.models import Workout
from .external_exercise import ExternalExercise


class Exercise(models.Model):
    class Meta:
        app_label = "api"

    name = models.CharField(max_length=150, null=False)
    sets = models.JSONField(null=False, default=dict)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    UNIT_CHOICES = [
        ("lbs", "lbs"),
        ("kg", "kg"),
        ("bw", "bw")
        ("timed", "timed"),
    ]
    unit = models.CharField(max_length=150, null=False, choices=UNIT_CHOICES)
    external_exercise = models.ForeignKey(
        ExternalExercise, on_delete=models.PROTECT, null=True, blank=True
    )
