from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from api.tasks import update_external_exercises
from api.serializers import ExternalExerciseSerializer
from api.models import ExternalExercise
import requests


class ExternalExerciseApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Need the api ninjas key in env to acess the exercises api
        # It's normal for this view to take a long time, http response may timeout
        ExternalExercise.objects.all().delete()
        muscle_groups = [
            "abdominals",
            "abductors",
            "adductors",
            "biceps",
            "calves",
            "chest",
            "forearms",
            "glutes",
            "hamstrings",
            "lats",
            "lower_back",
            "middle_back",
            "neck",
            "quadriceps",
            "traps",
            "triceps",
        ]
        difficulties = ["beginner", "intermediate", "expert"]
        exercises = []

        for muscle_group in muscle_groups:
            for difficulty in difficulties:
                response = requests.get(
                    f"https://api.api-ninjas.com/v1/exercises?type=strength&muscle={muscle_group}&difficulty={difficulty}",
                    headers={"X-API-KEY": f"{settings.API_NINJAS_KEY}"},
                )
                if response.ok and len(response.json()) > 0:
                    exercises.append(response.json()[0])
                elif not response.ok:
                    return Response(
                        data={"error": response.json()},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

        serializer = ExternalExerciseSerializer(data=exercises, many=True)
        if not serializer.is_valid():
            return
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

        exercise = ExternalExercise.objects.get(id=exercise_id)
        if exercise:
            exercise.favorite = not exercise.favorite
            exercise.save()
            return Response(data={"success": True}, status=status.HTTP_200_OK)

        return Response(
            data={"message": "exercise not found"}, status=status.HTTP_400_BAD_REQUEST
        )
