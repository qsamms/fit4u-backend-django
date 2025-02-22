from django.shortcuts import get_object_or_404, get_list_or_404
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from api.models import Workout, Exercise, ExternalExercise
from api.serializers import WorkoutSerializer, ExerciseSerializer
from api.utils import is_valid_workout


class WorkoutApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data

        if not is_valid_workout(data):
            return Response(
                data={"error": "invalid request body"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data["workout"]["user"] = request.user.id

        try:
            with transaction.atomic():
                workout_serializer = WorkoutSerializer(data=data.get("workout"))
                if not workout_serializer.is_valid():
                    raise Exception("error creating workout")

                workout = workout_serializer.save()
                exercises = data["workout"].get("exercises", [])

                for exercise in exercises:
                    exercise["workout"] = workout.id

                exercise_serializer = ExerciseSerializer(data=exercises, many=True)
                if not exercise_serializer.is_valid():
                    workout.delete()
                    raise Exception("error creating exercises")

                exercise_serializer.save()
                return Response(
                    data={"message": "Workout successfully saved"},
                    status=status.HTTP_200_OK,
                )
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        workout_id = kwargs.get("pk")

        instance = get_object_or_404(Workout, id=workout_id)
        instance.delete()
        return Response(
            data={"message": "workout successfully deleted"}, status=status.HTTP_200_OK
        )

    def patch(self, request, *args, **kwargs):
        data = request.data

        if not is_valid_workout(data):
            return Response(
                data={"error": "invalid request body"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data["workout"]["user"] = request.user.id
        workout_id = kwargs.get("pk")

        for exercise in data["workout"]["exercises"]:
            exercise["workout"] = workout_id

        try:
            with transaction.atomic():
                if workout_id:
                    workout_instance = get_object_or_404(Workout, id=workout_id)
                    serializer = WorkoutSerializer(
                        workout_instance, data=data.get("workout")
                    )

                    if not serializer.is_valid():
                        raise Exception("error creating workout")
                    serializer.save()

                    exercise_json = data.get("workout").get("exercises")
                    existing_exercises = [
                        x for x in exercise_json if x["id"] not in (None, "undefined")
                    ]
                    create_exercises = [
                        x for x in exercise_json if x["id"] in (None, "undefined")
                    ]
                    exercise_dict = {x["id"]: x for x in existing_exercises}
                    existing_exercise_objs = get_list_or_404(
                        Exercise,
                        id__in=[x["id"] for x in existing_exercises],
                        workout=workout_instance,
                    )

                    for exercise in existing_exercise_objs:
                        json = exercise_dict.get(exercise.id)
                        ee = json.get("external_exercise", exercise.external_exercise)
                        if isinstance(ee, int):
                            ee = ExternalExercise.objects.get(id=ee)
                        exercise.external_exercise = ee
                        exercise.name = json.get("name", exercise.name)
                        exercise.unit = json.get("unit", exercise.unit)
                        exercise.sets = json.get("sets", exercise.sets)
                        exercise.save()

                    for exercise in create_exercises:
                        exercise.pop("id")
                        serializer = ExerciseSerializer(data=exercise)
                        if not serializer.is_valid():
                            raise Exception("error creating new exercises")
                        serializer.save()

                    return Response(
                        data={"message": "workout successfully updated"},
                        status=status.HTTP_200_OK,
                    )
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        workout_id = kwargs.get("pk", None)

        if workout_id:
            workout = get_object_or_404(Workout, id=workout_id)
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
