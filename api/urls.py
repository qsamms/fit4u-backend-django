from django.urls import path
from api.views import (
    GoogleLoginApi,
    UserApiView,
    WorkoutApiView,
    LogoutApiView,
    UpdateExternalExerciseApiView,
    GoalApiView
)

urlpatterns = [
    path("auth/login/google/", GoogleLoginApi.as_view(), name="google_oauth"),
    path("logout/", LogoutApiView.as_view(), name="logout"),
    path("me/", UserApiView.as_view(), name="get_user"),
    path("workout/", WorkoutApiView.as_view(), name="workout"),
    path("goals/", GoalApiView.as_view(), name="goals"),
    path(
        "update-external-exercises/",
        UpdateExternalExerciseApiView.as_view(),
        name="update_external_exercises",
    ),
]
