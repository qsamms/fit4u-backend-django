from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


User = get_user_model()

class UserAPI(APIView):
    authentication_classes = [authentication.TokenAuthentication]

    # get a specific user object by email
    def get(self, request, *args, **kwargs):
        user_email = request.data["email"]
        user = get_object_or_404(User, email=user_email)
        return Response(data={
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        })