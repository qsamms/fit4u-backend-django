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
        workout_dict = {w["id"]: w for w in WorkoutSerializer(workouts, many=True).data}
        for workout in workouts:
            workout_json = workout_dict[workout.id]
            workout_json["exercises"] = ExerciseSerializer(
                workout.exercise_set, many=True
            ).data

        """
        Response json will look like this:
        
        analysis: {
          abdominals: {
              avgRating: ...,   // average rating user gave for exercises with this muscle group
              exercises: [
                  {
                    // exercise info (name, muscle, difficulty, etc.)
                    weights: ...   // list of weights the user has done for that exercise in the time frame provided
                  }
              ]
          }
          biceps: {
              ...
          }
          ...
        }
        """
        analysis_response = {}
        for muscle_group in settings.MUSCLE_GROUPS:
            rating_sum, count = 0, 0
            mg_exercises = {}
            for _, workout in workout_dict.items():
                for exercise in workout.get("exercises", []):
                    ee = get_object_or_404(
                        ExternalExercise, id=exercise.get("external_exercise")
                    )
                    if ee.muscle == muscle_group:
                        ee_json = ExternalExerciseSerializer(ee).data
                        analysis = analyze_sets(
                            exercise.get("sets", []), exercise.get("unit")
                        )
                        if ee_json["id"] in mg_exercises:
                            mg_exercises[ee.id]["weights"].append(
                                {
                                    "weight": analysis["max_lift"],
                                    "datetime": workout.get("datetime"),
                                }
                            )
                        else:
                            ee_json["weights"] = [
                                {
                                    "weight": analysis["max_lift"],
                                    "datetime": workout.get("datetime"),
                                }
                            ]
                            mg_exercises[ee.id] = ee_json

                        rating_sum += analysis.get("rating_sum")
                        count += analysis.get("count")

            avg_rating = rating_sum / count if count > 0 else 0
            analysis_response.update(
                {
                    f"{muscle_group}": {
                        "avg_rating": avg_rating,
                        "exercises": sorted(
                            mg_exercises.values(), key=lambda x: x["name"]
                        ),
                    }
                }
            )

        return Response(data={"analysis": analysis_response}, status=status.HTTP_200_OK)
