import concurrent.futures
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from api.serializers import ExternalExerciseSerializer
from api.models import ExternalExercise
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

        serializer = ExternalExerciseSerializer(data=[e for e in exercises if e is not None], many=True)
        if not serializer.is_valid():
            return Response(data={"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()

        return Response(
            data={"message": "Data saved successfully"}, status=status.HTTP_200_OK
        )

    def get(self, request, *args, **kwargs):
        exercises = ExternalExercise.objects.all()
        serializer = ExternalExerciseSerializer(exercises, many=True)

        favorite_exercises = ExternalExercise.objects.filter(favorite=True)
        favorite_serializer = ExternalExerciseSerializer(favorite_exercises, many=True)

        return Response(
            data={"exercises": serializer.data, "favorites": favorite_serializer.data},
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
