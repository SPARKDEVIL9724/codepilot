from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()

class UserAPITests(APITestCase):
    def setUp(self):
        self.password = "TestPassword1001!"
        self.user = User.objects.create_user(
            username="autoTestUser",
            email="test.email@example.com",
            password=self.password,
            github_username="testgithub",
            tech_stack="Python",
        )

    def test_register_user(self):
        response = self.client.post(
            "/api/auth/register/",
            {
                "username": "NewUser",
                "email": "new.email@example.com",
                "password": "NewPassword00001!",
                "github_username": "newgithub",
                "tech_stack": "Django DjangoRestFramework",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="NewUser").exists())
        self.assertNotIn("password", response.data)

    def test_login_with_username(self):
        response = self.client.post(
            "/api/auth/login/",
            {
                "identifier": "autoTestUser",
                "password": self.password
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)

    def test_login_with_email(self):
        response = self.client.post(
            "/api/auth/login/",
            {
                "identifier": "test.email@example.com",
                "password": self.password
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)

    def test_login_with_invalid_password(self):
        response = self.client.post(
            "/api/auth/login/",
            {
                "identifier": "autoTestUser",
                "password": "wrongPassword"
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_me_requires_authentication(self):
        response = self.client.get("/api/auth/me/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_view_profile(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get("/api/auth/me/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "autoTestUser")
        self.assertEqual(response.data["email"], "test.email@example.com")
        self.assertNotIn("password", response.data)

    def test_authencticated_user_can_update_profile(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(
            "/api/auth/me/",
            {
                "github_username": "updatedgithub",
                "tech_stack": "Django, React",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["github_username"], "updatedgithub")
        self.assertEqual(response.data["tech_stack"], "Django, React")

        self.user.refresh_from_db()
        self.assertEqual(self.user.github_username, "updatedgithub")

    def test_me_patch_requires_authentication(self):
        response = self.client.patch(
            "/api/auth/me/",
            {"tech_stack": "Python"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token_returns_new_access_token(self):
        login_response = self.client.post(
            "/api/auth/login/",
            {
                "identifier": "autoTestUser",
                "password": self.password
            },
            format="json",
        )

        refresh_token = login_response.data["refresh_token"]

        response = self.client.post(
            "/api/auth/refresh/",
            {"refresh": refresh_token},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_login_with_unknown_identifier(self):
        response = self.client.post(
            "/api/auth/login/",
            {
                "identifier": "UnknownUser",
                "password": "UnknownPassword",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_with_duplicae_username(self):
        response = self.client.post(
            "/api/auth/register/",
            {
                "username": "autoTestUser",
                "email": "test.emmail@example.com",
                "password": "SomePassword121!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_with_missing_username(self):
        response = self.client.post(
            "/api/auth/register/",
            {
                "email": "new.email@example.com",
                "password": "newPassword147@",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_refresh_with_invalid_token(self):
        response = self.client.post(
            "/api/auth/refresh/",
            {"refresh": "invalid_token"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_update_with_invalid_github_username(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(
            "/api/auth/me/",
            {"github_username": "x"*51},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
