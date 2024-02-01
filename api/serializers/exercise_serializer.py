from rest_framework import serializers
from api.models import Exercise, ExternalExercise

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Exercise
        fields = '__all__'

        external_exercise = serializers.PrimaryKeyRelatedField(queryset=ExternalExercise.objects.all(), required=False)
        reps = serializers.IntegerField(required=False) 
        datetime = serializers.DateTimeField(required=False)       
