from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from api.models import CustomUser


class LoginApiView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email", "")
        password = request.data.get("password", "")

        if CustomUser.objects.filter(
            email=email, password=password, is_oauth=False
        ).exists():
            user = CustomUser.objects.get(
                email=email, password=password, is_oauth=False
            )
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                data={"message": "Login successful", "token": token.key},
                status=status.HTTP_200_OK,
            )
        return Response(
            data={
                "error": "The provided credentials do not match any users in our system."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class SignUpApiView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email", "")
        password = request.data.get("password", "")
        first_name = request.data.get("first_name", "")
        last_name = request.data.get("last_name", "")

        if CustomUser.objects.filter(email=email).exists():
            return Response(
                data={
                    "error": "A user with that email already exists, please log in or use a different email to sign up"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        CustomUser.objects.create(
            email=email,
            username=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_oauth=False,
        )
        return Response(
            data={"message": "User created successfully"}, status=status.HTTP_200_OK
        )


class LogoutApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        token = Token.objects.get(user=user)
        token.delete()
        return Response(
            data={"message": "Logout successful"}, status=status.HTTP_200_OK
        )
