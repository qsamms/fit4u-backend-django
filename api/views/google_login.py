# views.py
from ..utils.google_oauth_utils import get_user_data
from django.shortcuts import redirect
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from api.models import CustomUser
from ..serializers.auth_serializer import GoogleAuthSerializer


class GoogleLoginApi(APIView):
    def get(self, request, *args, **kwargs):
        auth_serializer = GoogleAuthSerializer(data=request.GET)
        auth_serializer.is_valid(raise_exception=True)

        validated_data = auth_serializer.validated_data
        user_data = get_user_data(validated_data)

        user = CustomUser.objects.get(email=user_data["email"])
        token, _ = Token.objects.get_or_create(user=user)

        return redirect(f"{settings.BASE_APP_URL}?token={token}")
