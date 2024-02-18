from django.urls import path
from api.views import (
    GoogleLoginApi,
    UserApiView,
    WorkoutApiView,
    LogoutApiView,
    ExternalExerciseApiView,
    LoginApiView,
    SignUpApiView,
    ChangePasswordView,
    FavoriteExerciseApiView,
    WorkoutPlanApiView,
)

urlpatterns = [
    path("me/", UserApiView.as_view(), name="get_user"),
    path("auth/login/google/", GoogleLoginApi.as_view(), name="google_oauth"),
    path("login/", LoginApiView.as_view(), name="login"),
    path("sign-up/", SignUpApiView.as_view(), name="sign-up"),
    path("logout/", LogoutApiView.as_view(), name="logout"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("workout/", WorkoutApiView.as_view(), name="workouts"),
    path("workout/<int:pk>/", WorkoutApiView.as_view(), name="single_workout"),
    path(
        "external-exercises/",
        ExternalExerciseApiView.as_view(),
        name="external_exercises",
    ),
    path(
        "external-exercises/favorite/",
        FavoriteExerciseApiView.as_view(),
        name="favorite",
    ),
    path("workout-plan/", WorkoutPlanApiView.as_view(), name="workout_plan"),
    path("workout-plan/<int:pk>/", WorkoutPlanApiView.as_view(), name="workout_plan"),
]
