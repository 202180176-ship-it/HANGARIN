from django.core.management.base import BaseCommand
from faker import Faker
from django.utils import timezone
from todo.models import Task, Note, SubTask, Category, Priority
import random

class Command(BaseCommand):
    help = "Seed database with fake data"

    def handle(self, *args, **kwargs):
        fake = Faker()

        categories = list(Category.objects.all())
        priorities = list(Priority.objects.all())

        for _ in range(20):
            task = Task.objects.create(
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                status=fake.random_element(elements=["Pending", "In Progress", "Completed"]),
                deadline=timezone.make_aware(fake.date_time_this_month()),
                category=random.choice(categories),
                priority=random.choice(priorities),
            )

            # Add subtasks
            for _ in range(random.randint(2, 5)):
                SubTask.objects.create(
                    parent_task=task,
                    title=fake.sentence(nb_words=3),
                    status=fake.random_element(elements=["Pending", "In Progress", "Completed"])
                )

            # Add notes
            for _ in range(random.randint(1, 3)):
                Note.objects.create(
                    task=task,
                    content=fake.paragraph(nb_sentences=2)
                )

        self.stdout.write(self.style.SUCCESS("Fake data generated successfully!"))
