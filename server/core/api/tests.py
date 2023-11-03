from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import ServerUsers
from django.contrib.auth.models import User


# Create your tests here.
class APITestCaseBase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            username="ADMIN_USER", password="ADMIN_PASSWORD", email="admin@example.com"
        )

    def authenticate(self):
        self.client.force_authenticate(user=self.admin_user)

    def get_token(self):
        signin_url = reverse("signin-admin")
        response = self.client.post(
            signin_url, data={"username": "ADMIN_USER", "password": "ADMIN_PASSWORD"}
        )
        return response.data["accessToken"]


class SigninAdminViewTest(APITestCaseBase):
    def test_signin(self):
        url = reverse("signin-admin")
        response = self.client.post(
            url, {"username": "ADMIN_USER", "password": "ADMIN_PASSWORD"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SignupUserViewTest(APITestCaseBase):
    def test_signup(self):
        self.authenticate()
        url = reverse("create-user")
        response = self.client.post(
            url,
            {
                "username": "test",
                "password": "112233",
                "multiuser": 1,
                "customer_user": "admin",
                "status": "active",
                "traffic": 0,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class DeleteUserViewTest(APITestCaseBase):
    def test_delete_user(self):
        self.authenticate()
        user_to_delete = ServerUsers.objects.create(
            username="test",
            password="password",
            multiuser=1,
            customer_user="admin",
            status="active",
            traffic=0,
        )
        url = reverse("delete-user", kwargs={"username": user_to_delete.username})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserEditViewTest(APITestCaseBase):
    def test_edit_user(self):
        self.authenticate()
        url = reverse("edit-user")
        self.client_test_user = ServerUsers.objects.create(
            username="test",
            password="password",
            multiuser=1,
            customer_user="admin",
            status="active",
            traffic=0,
        )
        data = {
            "username": "test",
            "password": "newpassword",
            "email": "newemail@example.com",
            "mobile": "1234567890",
            "multiuser": 2,
            "traffic": 100,
            "end_date": "2023-12-31",
            "type_traffic": "mb",
            "status": "active",
            "desc": "new description",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "User Updated"})

        # Refresh the client_test_user instance from the database
        self.client_test_user.refresh_from_db()

        # Assert the fields were updated correctly
        self.assertEqual(self.client_test_user.password, "newpassword")
        self.assertEqual(self.client_test_user.email, "newemail@example.com")
        self.assertEqual(self.client_test_user.mobile, "1234567890")
        self.assertEqual(self.client_test_user.multiuser, 2)
        self.assertEqual(self.client_test_user.traffic, 100)
        self.assertEqual(self.client_test_user.status, "active")
        self.assertEqual(self.client_test_user.desc, "new description")
        self.assertEqual(self.client_test_user.end_date, "2023-12-31")

    def test_edit_non_existent_user(self):
        self.authenticate()
        url = reverse("edit-user")
        data = {
            "username": "test1",
            "password": "newpassword",
            "email": "newemail@example.com",
            "mobile": "1234567890",
            "multiuser": 2,
            "traffic": 100,
            "end_date": "2023-12-31",
            "type_traffic": "mb",
            "status": "active",
            "desc": "new description",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"message": "Not Exist User"})
