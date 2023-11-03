from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from django.contrib.auth import login, authenticate
from .token import get_tokens_for_user
from .models import Client, Traffic, Settings
from .serializers import (
    UserSerializer,
    ClientTestSerializer,
    ActivateDeactivateUserSerializer,
    SettingsSerializer,
    UserEditSerializer,
)
from scripts.status import main as Server
from scripts.filteringcheck import filtering
from scripts.sshmonitor import online
from scripts.createuser import create_user
from scripts.deleteuser import delete_user
from scripts.edituser import manage_user
from scripts.killuser import kill_user
from scripts.killpid import kill_pid


# USERS: Signup User
class SignupUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            result = create_user(serializer.validated_data)
            if "error" not in result:
                return Response(
                    {**serializer.data, **result}, status=status.HTTP_201_CREATED
                )
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# USERS: Edit user
class UserEditView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        serializer = UserEditSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            username = data["username"]

            traffic = (
                data["traffic"] * 1024
                if data["type_traffic"] == "gb"
                else data["traffic"]
            )
            try:
                user = Client.objects.get(username=username)
            except Client.DoesNotExist:
                return Response(
                    {"message": "Not Exist User"}, status=status.HTTP_404_NOT_FOUND
                )

            # Update the user data if the key exists in the validated data
            for key, value in data.items():
                if hasattr(user, key):
                    setattr(user, key, value)

            traffic = (
                data["traffic"] * 1024
                if data["type_traffic"] == "gb"
                else data["traffic"]
            )
            user.traffic = traffic

            user.save()

            # Additional processing
            result = manage_user(data)
            if "error" in result:
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({"message": "User Updated"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# USERS: Detail User
class DetailUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, username):
        try:
            return Client.objects.get(username=username)
        except Client.DoesNotExist:
            return None

    def get(self, request, username):
        user = self.get_object(username)
        if user is None:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


# USERS: Delete User
class DeleteUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, username):
        user_instance = Client.objects.filter(username=username).first()
        result = delete_user(username)
        if "error" in result:
            return Response(
                {"error": result["error"]}, status=status.HTTP_400_BAD_REQUEST
            )
        Traffic.objects.filter(username=user_instance).delete()
        user_instance.delete()
        return Response({"message": result["message"]}, status=status.HTTP_200_OK)


# USERS: Get all Users
class GetAllUsersView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        users = Client.objects.all()
        serializer = ClientTestSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# USERS: Toggle Active && Inactive User
class ActivateDeactivateUserView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    queryset = Client.objects.all()
    serializer_class = ActivateDeactivateUserSerializer
    lookup_field = "username"

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()

        current_status = instance.status
        new_status = "active" if current_status == "inactive" else "inactive"
        instance.status = new_status
        instance.save()
        data = {
            "username": instance.username,
            "password": instance.password,
            "activate": instance.status,
        }
        manage_user(data=data)
        return Response(
            {"message": f"User status changed to {new_status}"},
            status=status.HTTP_200_OK,
        )


# ADMIN: Kill user
class KillUserView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request, username):
        result = kill_user(username)
        if "error" in result:
            return Response(
                {"error": result["error"]}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response({"message": result["message"]}, status=status.HTTP_200_OK)


# ADMIN: Kill id
class KillPidView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pid):
        result = kill_pid(pid)
        if "error" in result:
            return Response(
                {"error": result["error"]}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response({"message": result["message"]}, status=status.HTTP_200_OK)


# ADMIN: Signin Admin
class SigninAdminView(APIView):
    def post(self, request):
        try:
            username = request.data["username"]
            password = request.data["password"]
        except KeyError:
            return Response(
                {"message": "Username and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            auth_data = get_tokens_for_user(request.user)
            return Response({**auth_data}, status=status.HTTP_200_OK)
        return Response(
            {"message": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


# ADMIN: Init Settings
class SettingInitial(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        settings = Settings.load()
        serializer = SettingsSerializer(settings)
        return Response(serializer.data)


# Server APIs
class ServerStatus(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        details = Server()
        return Response(details)


class ServerFiltering(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = filtering()
        return Response(data)


class ServerOnlineUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        users = online()
        return Response(users)


# Refresh Token
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            refresh_token = response.data["refresh"]
            access_token = response.data["access"]
            return Response(
                {
                    "refreshToken": refresh_token,
                    "accessToken": access_token,
                }
            )
        return response
