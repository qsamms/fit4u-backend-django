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
        # Getting all the exercises from api ninjas and creating the objects in db takes a long time, so
        # it's normal for this view to take > 20s to return a response. Could move this logic to a background task
        # but it's unnecessary since this data is collected once and read only then on.
        # Need the api ninjas key in your activate script in order to acess the exercises api
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
        return Response(data={"exercises": serializer.data}, status=status.HTTP_200_OK)
