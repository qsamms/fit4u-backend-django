from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from api.serializers import WorkoutPlanSerializer
from api.models import WorkoutPlan, ExternalExercise


class WorkoutPlanApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.data["workout_plan"]["user"] = request.user.id

        exercise_ids = set(request.data["workout_plan"].get("exercises", []))
        if not len(ExternalExercise.objects.filter(id__in=exercise_ids)) == len(exercise_ids):
            return Response(
                data={"error": "One or more provided exercise ids do not exist"}, status=status.HTTP_400_BAD_REQUEST
            )

        plan_serializer = WorkoutPlanSerializer(data=request.data.get("workout_plan"))
        if not plan_serializer.is_valid():
            return Response(
                data={
                    "error": "Error creating workout plan",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        plan_serializer.save()
        return Response(
            data={
                "message": "Workout plan created successfully",
            },
            status=status.HTTP_200_OK,
        )

    def patch(self, request, *args, **kwargs):
        plan_id = kwargs.get("pk", None)
        request.data["workout_plan"]["user"] = request.user.id

        instance = WorkoutPlan.objects.get(pk=plan_id)
        serializer = WorkoutPlanSerializer(instance, data=request.data.get("workout_plan"))

        if serializer.is_valid():
            serializer.save()
            return Response(data={"message": f"Workout plan {plan_id} updated successfully"}, status=status.HTTP_200_OK)

        return Response(data={"error": "invalid data"}, status=status.HTTP_400_BAD_REQUEST)


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
