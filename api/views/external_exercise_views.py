import concurrent.futures
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from api.serializers import ExternalExerciseSerializer
from api.models import ExternalExercise, Exercise
from api.utils import analyze_sets
import requests


def fetch_exercise(muscle_group, difficulty) -> dict | None:
    response = requests.get(
        f"https://api.api-ninjas.com/v1/exercises?type=strength&muscle={muscle_group}&difficulty={difficulty}",
        headers={"X-API-KEY": f"{settings.API_NINJAS_KEY}"},
    )

    if response.ok and len(response.json()) > 0:
        return response.json()[0]
    elif not response.ok:
        return None


class ExternalExerciseApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        ExternalExercise.objects.all().delete()

        exercises = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(fetch_exercise, muscle_group, difficulty)
                for muscle_group in settings.MUSCLE_GROUPS
                for difficulty in settings.DIFFICULTIES
            ]

            for future in concurrent.futures.as_completed(futures):
                try:
                    exercises.append(future.result())
                except Exception as e:
                    return Response(
                        data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
                    )

        serializer = ExternalExerciseSerializer(
            data=[e for e in exercises if e is not None], many=True
        )
        if not serializer.is_valid():
            return Response(
                data={"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()

        return Response(
            data={"message": "Data saved successfully"}, status=status.HTTP_200_OK
        )

    def get(self, request, *args, **kwargs):
        user = request.user

        ees = ExternalExercise.objects.all()
        serializer = ExternalExerciseSerializer(ees, many=True)

        for ee in serializer.data:
            exercises = Exercise.objects.filter(
                workout__user=user, external_exercise=ee.get("id")
            )
            max_lift = 0

            for exercise in exercises:
                analysis = analyze_sets(exercise.sets, user.pref_unit)
                max_lift = max(max_lift, analysis.get("max_lift"))

            if len(exercises) > 0:
                most_recent_exercise = exercises.latest("workout__datetime")
                analysis = analyze_sets(most_recent_exercise.sets, user.pref_unit)
                ee["most_recent"] = analysis.get("max_lift")

            if "most_recent" not in ee:
                ee["most_recent"] = 0
            ee["max_lift"] = max_lift

        return Response(
            data={"exercises": serializer.data},
            status=status.HTTP_200_OK,
        )


class FavoriteExerciseApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        exercise_id = request.data.get("id")

        exercise = get_object_or_404(ExternalExercise, id=exercise_id)
        exercise.favorite = not exercise.favorite
        exercise.save()
        return Response(data={"success": True}, status=status.HTTP_200_OK)
