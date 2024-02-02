from background_task import background
from django.conf import settings
from api.serializers import ExternalExerciseSerializer
from api.models import ExternalExercise
import requests


@background(schedule=1)
def update_external_exercises(muscle_groups, types):
    ExternalExercise.objects.all().delete()

    for type in types:
        for muscle_group in muscle_groups:
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

            serializer = ExternalExerciseSerializer(data=filtered_response, many=True)
            if not serializer.is_valid():
                return
            serializer.save()
