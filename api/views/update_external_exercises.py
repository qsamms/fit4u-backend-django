from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from api.tasks import update_external_exercises


class UpdateExternalExerciseApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
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

        update_external_exercises(muscle_groups, types)

        return Response(
            data={"message": "Data save scheduled"}, status=status.HTTP_200_OK
        )
