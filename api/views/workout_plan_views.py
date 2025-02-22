from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from api.serializers import WorkoutPlanSerializer
from api.models import WorkoutPlan, ExternalExercise
from api.utils import is_valid_workout_plan


class WorkoutPlanApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data

        if not is_valid_workout_plan(data):
            return Response(
                data={"error": "invalid request body"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data["workout_plan"]["user"] = request.user.id
        try:
            exercise_ids = set(data["workout_plan"].get("exercises", []))
            if len(ExternalExercise.objects.filter(id__in=exercise_ids)) != len(
                exercise_ids
            ):
                raise Exception("One or more provided exercise ids do not exist")

            plan_serializer = WorkoutPlanSerializer(data=data.get("workout_plan"))
            if not plan_serializer.is_valid():
                raise Exception("error creating workout plan")
            plan_serializer.save()

            return Response(
                data={
                    "message": "Workout plan created successfully",
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        plan_id = kwargs.get("pk", None)

        instance = get_object_or_404(WorkoutPlan, id=plan_id)
        instance.delete()
        return Response(
            data={"message": "workout plan deleted successfully"},
            status=status.HTTP_200_OK,
        )

    def patch(self, request, *args, **kwargs):
        plan_id = kwargs.get("pk", None)
        data = request.data

        if not is_valid_workout_plan(data):
            return Response(
                data={"error": "invalid request body"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            data["workout_plan"]["user"] = request.user.id
            exercise_ids = data["workout_plan"].get("exercises", [])
            if len(ExternalExercise.objects.filter(id__in=exercise_ids)) != len(
                exercise_ids
            ):
                raise Exception("One or more provided exercise ids do not exist")

            instance = get_object_or_404(WorkoutPlan, id=plan_id)
            serializer = WorkoutPlanSerializer(instance, data=data.get("workout_plan"))
            if not serializer.is_valid():
                raise Exception("invalid data")

            serializer.save()
            return Response(
                data={"message": f"Workout plan {plan_id} updated successfully"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        plan_id = kwargs.get("pk")

        if plan_id:
            object_exists = WorkoutPlan.objects.filter(pk=plan_id).exists()
            if not object_exists:
                return Response(
                    data={"error": "A workout with that id does not exist"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            workout = WorkoutPlan.objects.get(id=plan_id)
            plan_serialier = WorkoutPlanSerializer(workout)
            json_data = plan_serialier.data

            return Response(data={"workout_plan": json_data}, status=status.HTTP_200_OK)
        else:
            workouts = WorkoutPlan.objects.filter(user=request.user.id)
            plan_serialier = WorkoutPlanSerializer(workouts, many=True)
            json_data = plan_serialier.data

            return Response(
                data={"workout_plans": json_data}, status=status.HTTP_200_OK
            )
