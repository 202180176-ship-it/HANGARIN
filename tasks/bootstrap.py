import os
import shutil
import sqlite3
import threading
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command

_BOOTSTRAP_LOCK = threading.Lock()
_BOOTSTRAP_COMPLETE = False
_REQUIRED_TABLES = {
    "auth_user",
    "django_migrations",
    "django_session",
    "tasks_category",
    "tasks_note",
    "tasks_priority",
    "tasks_subtask",
    "tasks_task",
}


def _is_ephemeral_sqlite_database():
    return bool(getattr(settings, "EPHEMERAL_SQLITE_DATABASE", False))


def _sqlite_tables(db_path):
    if not db_path.exists():
        return set()

    with sqlite3.connect(db_path) as connection:
        rows = connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        ).fetchall()

    return {row[0] for row in rows}


def _ensure_parent_directory(db_path):
    db_path.parent.mkdir(parents=True, exist_ok=True)


def _copy_packaged_database_if_available(db_path):
    source_db = Path(settings.BASE_DIR) / "db.sqlite3"
    if source_db.exists() and not db_path.exists():
        shutil.copy2(source_db, db_path)


def _run_initial_setup():
    db_path = Path(settings.DATABASES["default"]["NAME"])
    _ensure_parent_directory(db_path)
    _copy_packaged_database_if_available(db_path)

    if not _REQUIRED_TABLES.issubset(_sqlite_tables(db_path)):
        call_command("migrate", interactive=False, run_syncdb=True, verbosity=0)

    from tasks.models import Category, Priority

    if not Priority.objects.exists() or not Category.objects.exists():
        call_command("seed_reference_data", verbosity=0)

    username = os.getenv("DJANGO_SUPERUSER_USERNAME", "").strip()
    password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "").strip()
    email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com").strip()

    if username and password:
        user_model = get_user_model()
        if not user_model.objects.filter(username=username).exists():
            user_model.objects.create_superuser(
                username=username,
                email=email,
                password=password,
            )


def ensure_serverless_database_ready():
    global _BOOTSTRAP_COMPLETE

    if _BOOTSTRAP_COMPLETE or not _is_ephemeral_sqlite_database():
        return

    with _BOOTSTRAP_LOCK:
        if _BOOTSTRAP_COMPLETE:
            return

        _run_initial_setup()
        _BOOTSTRAP_COMPLETE = True
