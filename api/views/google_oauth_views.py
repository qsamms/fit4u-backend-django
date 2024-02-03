# views.py
from django.shortcuts import redirect
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from api.models import CustomUser
from api.serializers import GoogleAuthSerializer
from api.utils import get_or_create_user


class GoogleLoginApi(APIView):
    def get(self, request, *args, **kwargs):
        auth_serializer = GoogleAuthSerializer(data=request.GET)
        auth_serializer.is_valid(raise_exception=True)

        validated_data = auth_serializer.validated_data
        user, _ = get_or_create_user(validated_data)

        token, _ = Token.objects.get_or_create(user=user)

        return redirect(f"{settings.BASE_APP_URL}?token={token.key}")
