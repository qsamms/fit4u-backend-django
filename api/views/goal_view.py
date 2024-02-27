from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from api.models import Exercise
from api.serializers import ExerciseSerializer

class GoalApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Get the exercise ID from the query parameters
        exercise_id = request.query_params.get("exerciseID")

        if exercise_id:
            # Find all exercises performed by the current user with the given exercise ID
            exercises = Exercise.objects.filter(workout__user=request.user.id, id=exercise_id)
            exercise_serializer = ExerciseSerializer(exercises, many=True)
            
            # Return the serialized exercises data
            return Response(data={"exercises": exercise_serializer.data}, status=status.HTTP_200_OK)
        else:
            # If no exercise ID is provided, return an error response
            return Response(data={"message": "Please provide a valid exerciseID"}, status=status.HTTP_400_BAD_REQUEST)
