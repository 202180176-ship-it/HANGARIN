from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.test import override_settings
from django.utils import timezone

from todo.models import Category, Note, Priority, SubTask, Task


class SeedHangarinCommandTests(TestCase):
    def test_seed_hangarin_creates_required_reference_and_fake_data(self):
        output = StringIO()

        call_command("seed_hangarin", "--tasks", "3", stdout=output)

        self.assertEqual(Category.objects.count(), 5)
        self.assertEqual(Priority.objects.count(), 5)
        self.assertTrue(
            get_user_model().objects.filter(username="hangarin_demo").exists()
        )
        self.assertEqual(Task.objects.count(), 3)
        self.assertGreaterEqual(SubTask.objects.count(), 6)
        self.assertGreaterEqual(Note.objects.count(), 3)

        allowed_statuses = {
            "Pending",
            "In Progress",
            "Completed",
        }
        for task in Task.objects.all():
            self.assertIn(task.status, allowed_statuses)
            self.assertTrue(timezone.is_aware(task.deadline))
            self.assertTrue(task.title)
            self.assertTrue(task.description)

        self.assertIn("Seeded 3 tasks", output.getvalue())

    def test_seed_data_alias_uses_same_command_behavior(self):
        user_model = get_user_model()
        user_model.objects.create_user(username="existing_user", password="testpass123")

        call_command("seed_data", "--tasks", "1", "--username", "existing_user")

        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().user.username, "existing_user")


class LoginPageTests(TestCase):
    def test_login_page_shows_background_login_and_disabled_social_buttons_when_missing(self):
        response = self.client.get("/login/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Email or Username")
        self.assertContains(response, "Continue with GitHub")
        self.assertContains(response, "Continue with Google")
        self.assertContains(response, "GOOGLE_OAUTH_CLIENT_ID")

    @override_settings(
        SOCIALACCOUNT_PROVIDERS={
            "google": {
                "SCOPE": ["profile", "email"],
                "APPS": [
                    {
                        "name": "Google",
                        "client_id": "google-client-id",
                        "secret": "google-client-secret",
                    }
                ],
            },
            "github": {
                "SCOPE": ["read:user", "user:email"],
                "APPS": [
                    {
                        "name": "GitHub",
                        "client_id": "github-client-id",
                        "secret": "github-client-secret",
                    }
                ],
            },
        }
    )
    def test_login_page_renders_google_and_github_buttons_when_configured(self):
        response = self.client.get("/login/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Continue with Google")
        self.assertContains(response, "Continue with GitHub")
        self.assertContains(response, "/accounts/google/login/")
        self.assertContains(response, "/accounts/github/login/")

    def test_login_accepts_email_address(self):
        user_model = get_user_model()
        user_model.objects.create_user(
            username="emailuser",
            email="emailuser@example.com",
            password="testpass123",
        )

        response = self.client.post(
            "/login/",
            {"username": "emailuser@example.com", "password": "testpass123"},
        )

        self.assertEqual(response.status_code, 302)
