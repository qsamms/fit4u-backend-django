from django.db import models


class ExternalExercise(models.Model):
    class Meta:
        app_label = "api"

    name = models.CharField(max_length=150, null=False)
    exercise_type = models.CharField(max_length=150, null=False)
    muscle = models.CharField(max_length=150, null=False)
    equipment = models.CharField(max_length=150, null=False)
    difficulty = models.CharField(max_length=150, null=False)
    instructions = models.TextField()
