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


class UpdateExternalExerciseApiView(APIView):
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
        types = ["strength", "cardio", "stretching"]
        responses = []

        for muscle_group in muscle_groups:
            for type in types:
                response = requests.get(
                    f"https://api.api-ninjas.com/v1/exercises?type={type}&muscle={muscle_group}",
                    headers={"X-API-KEY": f"{settings.API_NINJAS_KEY}"},
                )
                if response.ok:
                    names = set()
                    for exercise in response.json():
                        name = exercise.get("name")
                        if name not in names:
                            responses.append(exercise)
                        names.add(name)
                else:
                    return Response(data={"error": response.json()}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ExternalExerciseSerializer(
                    data=responses, many=True
                )
        if not serializer.is_valid():
            return
        serializer.save()

        return Response(
            data={"message": "Data saved successfully"}, status=status.HTTP_200_OK
        )
