from django.urls import path, include
from api.views.google_login import GoogleLoginApi
from api.views.user_views import UserApiView
from api.views.workout_views import WorkoutApiView

urlpatterns = [
    path('auth/login/google/', GoogleLoginApi.as_view(), name='google_oauth'),
    path('me/', UserApiView.as_view(), name='get_user'),
    path('workout/', WorkoutApiView.as_view(), name='workout')
]