from django.urls import path, include
from api.views import GoogleLoginApi, UserApiView, WorkoutApiView, LogoutApiView

urlpatterns = [
    path("auth/login/google/", GoogleLoginApi.as_view(), name="google_oauth"),
    path("logout/", LogoutApiView.as_view(), name="logout"),
    path("me/", UserApiView.as_view(), name="get_user"),
    path("workout/", WorkoutApiView.as_view(), name="workout"),
]
