from django.db import models
from api.models import Workout
from .external_exercise import ExternalExercise

class Exercise(models.Model): 
    class Meta:
        app_label = 'api'

    name = models.CharField(max_length=150, null=False)
    set_number = models.IntegerField(null=False)
    reps = models.IntegerField(null=True, blank=True)
    volume = models.IntegerField(null=True, blank=True)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    rating = models.IntegerField(null=False, blank=False)
    datetime = models.DateTimeField(null=True, blank=True)
    UNIT_CHOICES = [
        ('lbs', 'lbs'), ('kg', 'kg'), ('sec', 'sec'), ('min', 'min'), ('pounds', 'pounds'), ('kilograms', 'kilograms'), ('seconds', 'seconds'), ('minutes', 'minutes'), ('hours', 'hours'), ('hrs', 'hrs')
    ]
    unit = models.CharField(max_length=150, null=False, choices=UNIT_CHOICES)
    external_exercise = models.ForeignKey(ExternalExercise, on_delete=models.PROTECT, null=True, blank=True)