# views.py
from ..utils.google_oauth_utils import get_user_data
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth import login
from rest_framework.views import APIView
from ..models.custom_user import CustomUser
from ..serializers.auth_serializer import AuthSerializer

class GoogleLoginApi(APIView):
    def get(self, request, *args, **kwargs):
        auth_serializer = AuthSerializer(data=request.GET)
        auth_serializer.is_valid(raise_exception=True)
        
        validated_data = auth_serializer.validated_data
        user_data = get_user_data(validated_data)
        
        user = CustomUser.objects.get(email=user_data['email'])
        login(request, user)

        return redirect(settings.BASE_APP_URL)