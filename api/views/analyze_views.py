from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from api.models import Workout, ExternalExercise
from api.serializers import (
    WorkoutSerializer,
    ExerciseSerializer,
    ExternalExerciseSerializer,
)
from api.utils import analyze_sets
from datetime import timedelta


class AnalyzeApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        days = int(request.GET.get("days", 7))
        user = request.user.id
        # get all workouts within the given time frame
        workouts = (
            Workout.objects.prefetch_related("exercise_set")
            .filter(
                datetime__gte=(timezone.now().date() - timedelta(days=days)), user=user
            )
            .all()
        )

        # get the associated exercises for each workout
        workout_dict = {
            w.get("id"): w for w in WorkoutSerializer(workouts, many=True).data
        }
        for workout in workouts:
            workout_json = workout_dict[workout.id]
            workout_json["exercises"] = ExerciseSerializer(
                workout.exercise_set, many=True
            ).data

        # response will look like this
        # analysis: {
        #   abdominals: {
        #       avgRating: ...,
        #       exercises: [
        #           {
        #           deserialized external exercise info...
        #           weights: [] list of weights the user has done for that exercise in the time frame provided
        #           }
        #       ]
        #   }
        #   biceps: {
        #       ...
        #   }
        #   ...
        # }
        mg_dict = {}
        for muscle_group in settings.MUSCLE_GROUPS:
            rating_sum, rating_num = 0, 0
            exercises = {}
            for _, workout in workout_dict.items():
                for exercise in workout.get("exercises", []):
                    ee = get_object_or_404(
                        ExternalExercise, id=exercise.get("external_exercise")
                    )
                    if ee.muscle == muscle_group:
                        ee_json = ExternalExerciseSerializer(ee).data
                        analysis = analyze_sets(exercise.get("sets", []))
                        largest_weight = analysis.get("largest_weight")
                        if exercises.get(ee_json.get("id"), None) is not None:
                            exercises[ee.id].get("weights").append(largest_weight)
                        else:
                            exercises[ee.id] = ee_json
                            ee_json["weights"] = []
                            exercises[ee.id].get("weights").append(largest_weight)

                        rating_sum += analysis.get("rating_sum")
                        rating_num += analysis.get("rating_num")

            avg_rating = rating_sum / rating_num if rating_num > 0 else 0
            mg_dict.update(
                {
                    f"{muscle_group}": {
                        "avg_rating": avg_rating,
                        "exercises": exercises.values(),
                    }
                }
            )

        return Response(data={"analysis": mg_dict}, status=status.HTTP_200_OK)
