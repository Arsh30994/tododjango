# Taskmate

Taskmate is a Django web app for personal to-do lists. Register an account, sign in, and manage your own tasks from a Bootstrap UI.

The project package name is `taskmate`. This repository is a small portfolio-style Django project, not a packaged library.

## Features

These features are implemented in the current codebase:

- **User registration** with username, email, and password (`users_app` + Django’s `User` model)
- **Login and logout** via Django’s built-in auth views
- **Per-user task lists** — each task is owned by the signed-in user (`TaskList.manage`)
- **Create, edit, and delete** tasks
- **Mark tasks completed or pending**
- **Ownership checks** on edit, delete, complete, and pending actions (other users’ tasks are rejected)
- **Pagination** — 5 tasks per page
- **Flash messages** for success and error feedback
- **Public home** (`/`) and **about** (`/about/`) pages
- **Contact page** (`/contact/`) — login required
- **Django admin** for the `TaskList` model
- **Optional PostgreSQL** when a database name is provided; otherwise SQLite

There is no REST API, no email verification, and no password-reset flow.

## Tech stack

| Layer | Choice |
| --- | --- |
| Language | Python 3.12+ (Django 6.0) |
| Framework | Django 6.0.1 |
| Config | [django-environ](https://django-environ.readthedocs.io/) |
| Forms | django-crispy-forms + crispy-bootstrap5 (login and register) |
| Frontend | Bootstrap 4.6.2 and jQuery from CDN; project templates |
| Database | SQLite by default; PostgreSQL via `psycopg2-binary` when configured |
| Server | Django development server (`manage.py runserver`); WSGI/ASGI entry points are included |

Pinned versions live in [`requirements.txt`](requirements.txt).

## Project structure

```text
.
├── manage.py                 # Django CLI
├── requirements.txt          # Pinned Python dependencies
├── taskmate/                 # Project settings and root URLconf
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── todolist_app/             # Tasks: model, views, forms, templates
├── users_app/                # Registration, login, logout templates
├── templates/                # Shared base template
│   └── base.html
├── static/                   # Logo and home-page image
│   └── css/js/image/
└── tmenv/                    # Leftover Windows venv — do not use
```

`users_app` does not define a custom user model. It uses `django.contrib.auth.models.User` and a `CustomUserCreationForm` that requires email.

## Data model

`todolist_app.models.TaskList` (admin label: Task):

| Field | Type | Notes |
| --- | --- | --- |
| `id` | `AutoField` | Primary key |
| `manage` | `ForeignKey` → `User` | Owner; `null=True`, `blank=True`; cascade delete |
| `title` | `CharField(200)` | Set automatically from the task text when omitted |
| `task` | `CharField(300)` | Task description shown in the UI |
| `done` | `BooleanField` | Default `False` |

The add-task form on `/todolist/` posts the `task` field. If `title` is empty, the view and form fill it with the first 200 characters of `task`.

## Routes

| Path | Auth | View |
| --- | --- | --- |
| `/` | Public | Home |
| `/todolist/` | Login required | List and add tasks |
| `/todolist/edit/<task_id>/` | Login required | Edit a task you own |
| `/todolist/delete/<task_id>/` | Login required | Delete a task you own |
| `/todolist/complete/<task_id>/` | Login required | Mark completed |
| `/todolist/pending/<task_id>/` | Login required | Mark pending |
| `/account/register/` | Public | Register |
| `/account/login/` | Public | Login |
| `/account/logout/` | Auth view | Logout (`LogoutView`, POST only; GET returns 405) |
| `/contact/` | Login required | Contact page |
| `/about/` | Public | About page |
| `/admin/` | Staff | Django admin |

After a successful login, Django redirects to `todolist`. Logout is Django’s `LogoutView` and accepts **POST** only (GET returns HTTP 405). After a successful logout, Django redirects to `login`. Unauthenticated visits to login-required pages go to `/account/login/`.

## Getting started

### Prerequisites

- Python 3.12 or newer
- `pip`
- Optional: PostgreSQL, only if you set `DJANGO_DB_NAME`

A `tmenv/` directory is committed from a Windows machine. Ignore it and create a new virtual environment on your system.

On Debian/Ubuntu, `python3 -m venv` needs the `python3-venv` package (`sudo apt install python3.12-venv`). If that package is unavailable, `pip install virtualenv` and `virtualenv .venv` work the same way.

### Local setup (SQLite)

`requirements.txt` is UTF-16 (saved from Windows). On Linux and macOS, `pip install -r requirements.txt` typically fails with `Invalid requirement`; convert a UTF-8 copy first. On Windows you can install from `requirements.txt` directly.

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# Linux / macOS (UTF-16 → UTF-8). Skip this block on Windows.
python3 -c "from pathlib import Path; Path('requirements.utf8.txt').write_text(Path('requirements.txt').read_bytes().decode('utf-16'))"
pip install -r requirements.utf8.txt

# Windows:
# pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

A `.env` file is **not** required for local development. Settings fall back to SQLite (`db.sqlite3` in the project root) and a development secret key. `requirements.utf8.txt` is a local conversion file; do not commit it.

### Create an admin user (optional)

```bash
python manage.py createsuperuser
```

Then sign in at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) to inspect `TaskList` records.

### Typical first run in the browser

1. Open the home page and go to **Register**.
2. Create an account (username, email, password).
3. Log in. You are sent to `/todolist/`.
4. Add tasks, mark them complete or pending, edit, or delete them.

## Environment variables

`taskmate/settings.py` loads a `.env` file from the project root via `django-environ` if that file exists. `.env` is gitignored.

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `DJANGO_SECRET_KEY` | No | `django-insecure-dev-key-change-in-production` | Django secret key. Change this for any shared or production deploy. |
| `DJANGO_SECERET_KEY` | No | — | Misspelled fallback read only if `DJANGO_SECRET_KEY` is unset. Prefer `DJANGO_SECRET_KEY`. |
| `DJANGO_DEBUG` | No | `True` | Debug flag (`True` / `False`). |
| `DJANGO_ALLOWED_HOSTS` | No | `localhost,127.0.0.1,testserver` | Comma-separated hostnames. |
| `DJANGO_DB_NAME` | No | unset | If **set**, Django uses PostgreSQL instead of SQLite. |
| `DJANGO_DB_USER` | No | empty | PostgreSQL user (used only when `DJANGO_DB_NAME` is set). |
| `DJANGO_DB_PASSWORD` | No | empty | PostgreSQL password. |
| `DJANGO_DB_HOST` | No | `localhost` | PostgreSQL host. |
| `DJANGO_DB_PORT` | No | `5432` | PostgreSQL port. |

Example `.env` for SQLite development:

```env
DJANGO_SECRET_KEY=replace-me
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

Example `.env` for PostgreSQL:

```env
DJANGO_SECRET_KEY=replace-me
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_DB_NAME=taskmate
DJANGO_DB_USER=taskmate
DJANGO_DB_PASSWORD=replace-me
DJANGO_DB_HOST=localhost
DJANGO_DB_PORT=5432
```

`STATIC_ROOT` is not configured. `collectstatic` is not part of the local workflow; `DEBUG=True` serves files from `static/` via `STATICFILES_DIRS`.

## Configuration notes

- **Timezone:** `UTC`
- **Language:** `en-us`
- **Crispy Forms pack:** `bootstrap5` (login/register forms). Page chrome uses Bootstrap 4.6.2 from the CDN in `templates/base.html`.
- **Tests:** `todolist_app/tests.py` and `users_app/tests.py` are Django stubs and do not contain assertions.

## License

No license file is included in this repository.
