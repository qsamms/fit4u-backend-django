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

        for muscle_group in muscle_groups:
            for type in types:
                response = requests.get(
                    f"https://api.api-ninjas.com/v1/exercises?type={type}&muscle={muscle_group}",
                    headers={"X-API-KEY": f"{settings.API_NINJAS_KEY}"},
                )
                names = set()
                filtered_response = []
                for data in response.json():
                    name = data.get("name")
                    if name not in names:
                        filtered_response.append(data)
                    names.add(name)

                serializer = ExternalExerciseSerializer(
                    data=filtered_response, many=True
                )
                if not serializer.is_valid():
                    return
                serializer.save()

        return Response(
            data={"message": "Data saved successfully"}, status=status.HTTP_200_OK
        )
