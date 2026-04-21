# Hangarin — Task & To-Do Manager (Django)

## Problem statement
"polish all the ui of it then give me the working app of it" — starting from an existing Django task manager (Hangarin) with Tasks, SubTasks, Categories, Priorities, Notes.

## User choices (captured via ask_human)
- UI: Distinctive polished look (glassmorphic dark + clean productivity) — we chose editorial dark-ink + warm cream + amber/teal accents, no purple AI-slop.
- Keep existing page structure.
- OAuth: Placeholder wired; user will provide Google/GitHub keys later via `.env`.
- Admin credentials: **RICHO / RICH12345**.
- Auto-seed sample data: enabled.
- Deployment target: Vercel (settings already support PostgreSQL via `DATABASE_URL`).

## Architecture
- Django 5.2 + django-allauth + django-pwa
- SQLite in dev (preview), PostgreSQL on Vercel via `DATABASE_URL`
- Supervisor runs Django on port 3000 so the Kubernetes ingress serves all routes

## What's been implemented (Apr 21, 2026)
- Full UI polish: consolidated `tasks/static/tasks/theme.css` with editorial serif + warm cream canvas + deep ink sidebar + amber CTAs + mono micro-labels
- Templates refined: `base.html`, `login.html`, `dashboard.html`, `entity_list.html`, `entity_form.html`
- Legacy `material-admin.css` neutralized
- `data-testid` attributes added across interactive UI
- Migrations + seed_reference_data + seed_fake_data (18 tasks, subtasks, notes) executed
- Superuser `RICHO` created

## Backlog (P1 / P2)
- Wire real Google / GitHub OAuth keys when user provides them
- Vercel deployment: set `DATABASE_URL`, `DJANGO_SECRET_KEY`, `CSRF_TRUSTED_ORIGINS` for live domain
- Add bulk actions on Tasks list (complete multiple, delete)
- Optional: Task detail view with subtasks + notes in one place

## Enhancement suggestion
Add a "Daily Focus" widget on Dashboard that highlights the single highest-priority task due soonest — raises daily return-engagement for a productivity app.
