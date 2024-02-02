from django.urls import path
from api.views import (
    GoogleLoginApi,
    UserApiView,
    WorkoutApiView,
    LogoutApiView,
    UpdateExternalExerciseApiView,
    SingleWorkoutApiView,
)

urlpatterns = [
    path("me/", UserApiView.as_view(), name="get_user"),
    path("auth/login/google/", GoogleLoginApi.as_view(), name="google_oauth"),
    path("logout/", LogoutApiView.as_view(), name="logout"),
    path("workout/", WorkoutApiView.as_view(), name="workout"),
    path("workout/<int:pk>/", SingleWorkoutApiView.as_view(), name="single_workout"),
    path(
        "update-external-exercises/",
        UpdateExternalExerciseApiView.as_view(),
        name="update_external_exercises",
    ),
]
