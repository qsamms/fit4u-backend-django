from rest_framework import serializers
from api.models import WorkoutPlan, ExternalExercise
from api.serializers import ExternalExerciseSerializer


class WorkoutPlanSerializer(serializers.ModelSerializer):
    exercises = serializers.ListField(write_only=True)

    class Meta:
        model = WorkoutPlan
        fields = "__all__"

    def create(self, validated_data):
        exercises_data = validated_data.pop("exercises", [])
        workout_plan = WorkoutPlan.objects.create(**validated_data)

        for exercise_id in exercises_data:
            exercise = ExternalExercise.objects.get(pk=exercise_id)
            workout_plan.exercises.add(exercise)

        return workout_plan

    def to_representation(self, instance):
        sup = super().to_representation(instance)

        sup["exercises"] = []
        for exercise in instance.exercises.all():
            sup["exercises"].append(ExternalExerciseSerializer(exercise).data)

        return sup
