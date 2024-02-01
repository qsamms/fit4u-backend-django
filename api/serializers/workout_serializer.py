from rest_framework import serializers
from api.models import Workout
from .exercise_serializer import ExerciseSerializer

class WorkoutSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Workout
        fields = '__all__'