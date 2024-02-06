from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from api.models import CustomUser
from api.serializers import LoginSerializer, SignUpSerializer


class LoginApiView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data={"error": "Both email and password fields are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        email = serializer.validated_data.get("email", "")
        password = serializer.validated_data.get("password", "")

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
        serializer = SignUpSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data={"error": "All sign-up form fields are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        email = serializer.validated_data.get("email", "")
        password = serializer.validated_data.get("password", "")
        first_name = serializer.validated_data.get("first_name", "")
        last_name = serializer.validated_data.get("last_name", "")

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
        Token.objects.get(user=request.user).delete()
        return Response(
            data={"message": "Logout successful"}, status=status.HTTP_200_OK
        )


class ChangePasswordView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        user = request.user

        if old_password != user.password:
            return Response(
                data={"error": "old password does not match"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.password = new_password
        user.save()
        return Response(
            data={"message": "user updated successfully"}, status=status.HTTP_200_OK
        )
