from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from api.models import CustomUser, ExternalExercise


class WorkoutTests(TestCase):
    def setUp(self):
        user = CustomUser.objects.create(
            username="testuser", email="testuser@gmail.com"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        self.exercise = ExternalExercise.objects.create(
            name="Bench Press", type="strength", difficulty="begineer"
        )

    def test_create_workout(self):
        valid_json = {
            "workout": {
                "name": "Chest Day",
                "datetime": "2024-02-01T11:00:00",
                "exercises": [
                    {
                        "external_exercise": self.exercise.id,
                        "name": "Bench Press",
                        "unit": "lbs",
                        "sets": [
                            {"setNumber": 1, "reps": 10, "volume": 135, "rating": 5},
                            {"setNumber": 2, "reps": 10, "volume": 135, "rating": 7},
                        ],
                    }
                ],
            }
        }
        response = self.client.post("/api/workout/", data=valid_json, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        invalid_json = {}
        response = self.client.post("/api/workout/", data=invalid_json, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
