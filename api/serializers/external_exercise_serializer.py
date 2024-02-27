from rest_framework import serializers
from api.models import ExternalExercise


class ExternalExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalExercise
        fields = "__all__"

    instructions = serializers.CharField(
        max_length=None, required=False, allow_blank=True
    )
    favorite = serializers.BooleanField(default=False)
