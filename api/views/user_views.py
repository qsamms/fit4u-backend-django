from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class UserApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response(
            data={
                "username": request.user.username,
                "email": request.user.email,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "preferred_unit": request.user.pref_unit,
            },
            status=status.HTTP_200_OK,
        )

    def patch(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        user.pref_unit = data.get("unit")
        user.save()
        return Response(
            data={"message": "user updated successfully"}, status=status.HTTP_200_OK
        )
