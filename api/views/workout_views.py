from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from api.models import Workout, Exercise
from api.serializers import WorkoutSerializer, ExerciseSerializer


class WorkoutApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        if "workout" not in data:
            return Response(data={"error": "invalid request body"}, status=status.HTTP_400_BAD_REQUEST)
        request.data["workout"]["user"] = request.user.id

        workout_serializer = WorkoutSerializer(data=data.get("workout"))
        if not workout_serializer.is_valid():
            return Response(
                data={
                    "error": "Error creating workout",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        workout = workout_serializer.save()

        exercises = data["workout"].get("exercises", [])
        for exercise in exercises:
            exercise["workout"] = workout.id

        exercise_serializer = ExerciseSerializer(data=exercises, many=True)
        if not exercise_serializer.is_valid():
            workout.delete()
            return Response(
                data={
                    "error": "Error creating exercises",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        exercise_serializer.save()
        return Response(
            data={"message": "Workout successfully saved"}, status=status.HTTP_200_OK
        )

    def get(self, request, *args, **kwargs):
        workout_id = kwargs.get("pk")

        if workout_id:
            object_exists = Workout.objects.filter(pk=workout_id).exists()
            if not object_exists:
                return Response(
                    data={"error": "A workout with that id does not exist"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            workout = Workout.objects.get(id=workout_id)
            workout_serialier = WorkoutSerializer(workout)
            workout_data = workout_serialier.data

            exercises = Exercise.objects.filter(workout=workout.id)
            exercise_serializer = ExerciseSerializer(exercises, many=True)
            workout_data["exercises"] = exercise_serializer.data

            return Response(data={"workout": workout_data}, status=status.HTTP_200_OK)
        else:
            workouts = Workout.objects.filter(user=request.user.id).order_by(
                "-datetime"
            )
            workout_serialier = WorkoutSerializer(workouts, many=True)
            workout_data = workout_serialier.data

            for workout in workout_data:
                workout_id = workout.get("id")
                exercises = Exercise.objects.filter(workout=workout_id)
                exercise_serializer = ExerciseSerializer(exercises, many=True)
                workout["exercises"] = exercise_serializer.data

            return Response(data={"workouts": workout_data}, status=status.HTTP_200_OK)
