from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Category, Note, Priority, StatusChoices, SubTask, Task


class FrontendViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="viewer",
            password="safe-password-123",
        )
        cls.category = Category.objects.create(name="Operations")
        cls.priority = Priority.objects.create(name="High")
        cls.task = Task.objects.create(
            title="Finish runway audit",
            description="Finalize the operational runway checklist.",
            status=StatusChoices.IN_PROGRESS,
            deadline=timezone.now() + timedelta(days=2),
            category=cls.category,
            priority=cls.priority,
        )
        SubTask.objects.create(
            task=cls.task,
            title="Collect field signatures",
            status=StatusChoices.PENDING,
        )
        Note.objects.create(
            task=cls.task,
            content="Pending approval from the hangar supervisor.",
        )

    def test_home_redirects_to_login_for_anonymous_users(self):
        response = self.client.get(reverse("tasks:home"))
        self.assertRedirects(response, reverse("tasks:login"))

    def test_login_redirects_to_dashboard(self):
        response = self.client.post(
            reverse("tasks:login"),
            {"username": "viewer", "password": "safe-password-123"},
        )
        self.assertRedirects(response, reverse("tasks:dashboard"))

    def test_dashboard_renders_backend_data(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("tasks:dashboard"))
        self.assertContains(response, "Finish runway audit")
        self.assertContains(response, "In Progress")

    def test_task_list_search_filters_results(self):
        Task.objects.create(
            title="Archive finance logs",
            description="Back office cleanup.",
            status=StatusChoices.COMPLETED,
            category=self.category,
            priority=self.priority,
        )
        self.client.force_login(self.user)
        response = self.client.get(reverse("tasks:task-list"), {"q": "runway"})
        self.assertContains(response, "Finish runway audit")
        self.assertNotContains(response, "Archive finance logs")

    def test_logout_uses_post_and_redirects_to_login(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("tasks:logout"))
        self.assertRedirects(response, reverse("tasks:login"))

    def test_frontend_task_create_persists_record(self):
        self.client.force_login(self.user)
        deadline = (timezone.localtime(timezone.now()) + timedelta(days=1)).strftime(
            "%Y-%m-%dT%H:%M"
        )
        response = self.client.post(
            reverse("tasks:task-create"),
            {
                "title": "Launch safety review",
                "description": "Prepare the final frontend-connected review.",
                "status": StatusChoices.PENDING,
                "category": self.category.pk,
                "priority": self.priority.pk,
                "deadline": deadline,
            },
        )
        self.assertRedirects(response, reverse("tasks:task-list"))
        self.assertTrue(Task.objects.filter(title="Launch safety review").exists())
