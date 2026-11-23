# InternTrack

[![CI](https://github.com/gundatharuntej2006-hue/InternTrack/actions/workflows/ci.yml/badge.svg)](https://github.com/gundatharuntej2006-hue/InternTrack/actions/workflows/ci.yml)

Internship and Training Management System for One University Department.

> **Status:** DT-1 (project foundation) and DT-2 (CI). This sets up the
> Django project, a PostgreSQL database in Docker, environment-based
> configuration, a `/health/` endpoint, and GitHub Actions CI that runs the
> tests on every push and pull request. Feature modules come in later
> milestones.

---

## Table of contents

1. [Project overview](#1-project-overview)
2. [Technology stack](#2-technology-stack)
3. [Prerequisites](#3-prerequisites)
4. [Repository setup](#4-repository-setup)
5. [Environment configuration](#5-environment-configuration)
6. [Start PostgreSQL with Docker](#6-start-postgresql-with-docker)
7. [Install dependencies and run migrations](#7-install-dependencies-and-run-migrations)
8. [Start the Django server](#8-start-the-django-server)
9. [Health endpoint](#9-health-endpoint)
10. [Running tests](#10-running-tests)
11. [Common errors and solutions](#11-common-errors-and-solutions)
12. [Project structure](#12-project-structure)
13. [Daily workflow cheat sheet](#13-daily-workflow-cheat-sheet)
14. [Team Git workflow](#14-team-git-workflow)
15. [Continuous integration (CI)](#15-continuous-integration-ci)

**Short on time?** Jump to the [Quick start](#quick-start-tldr).

---

## Quick start (TL;DR)

Make sure Docker Desktop is running, then run the commands for your OS.

**Windows (PowerShell)**

```powershell
git clone https://github.com/gundatharuntej2006-hue/InternTrack.git
cd InternTrack
Copy-Item .env.example .env          # then edit .env (see section 5)
docker compose up -d --wait
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**macOS / Linux**

```bash
git clone https://github.com/gundatharuntej2006-hue/InternTrack.git
cd InternTrack
cp .env.example .env                 # then edit .env (see section 5)
docker compose up -d --wait
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open <http://127.0.0.1:8000/health/>. You should see:

```json
{"status": "ok", "database": "ok"}
```

---

## 1. Project overview

InternTrack helps one university department manage student internships and
training. The current milestone (DT-1) provides only the technical
foundation that every later feature is built on:

- A Django project with environment-based settings.
- PostgreSQL running locally in Docker.
- A `/health/` endpoint that confirms Django is running **and** the
  database is reachable.
- Automated tests.

## 2. Technology stack

| Layer            | Technology                         | Version          |
|------------------|------------------------------------|------------------|
| Language         | Python                             | 3.11 (3.10–3.13 supported) |
| Web framework    | Django (LTS)                       | 5.2.19           |
| Database         | PostgreSQL (Docker image `postgres:17-alpine`) | 17   |
| DB driver        | psycopg 3 (binary)                 | 3.3.9            |
| Configuration    | django-environ (reads `.env`)      | 0.14.0           |
| Containers       | Docker + Docker Compose v2         | Compose v2+      |

Exact Python package versions are pinned in [`requirements.txt`](requirements.txt).

## 3. Prerequisites

Install these once. Check each with the command shown.

| Tool | Check | Get it |
|------|-------|--------|
| Git | `git --version` | <https://git-scm.com/downloads> |
| Python 3.11+ | `python --version` (macOS/Linux: `python3 --version`) | <https://www.python.org/downloads/>. **Windows:** tick "Add python.exe to PATH" in the installer. |
| Docker Desktop (includes Compose) | `docker --version` and `docker compose version` | <https://www.docker.com/products/docker-desktop/> |
| GitHub access | You must be added as a collaborator (the repo is **private**) | Ask the repository owner |

> **Docker Desktop must be running** (whale icon in the system tray / menu
> bar, status "Engine running") before any `docker compose` command.

You do **not** need to install PostgreSQL itself. Docker provides it.

## 4. Repository setup

```bash
git clone https://github.com/gundatharuntej2006-hue/InternTrack.git
cd InternTrack
```

Because the repository is private, Git will ask you to sign in. The easiest
option is the GitHub CLI: run `gh auth login` once, or sign in through the
browser window Git for Windows opens.

All commands below are run **from the `InternTrack` folder** (the one
containing `manage.py`).

## 5. Environment configuration

All configuration (secrets, database credentials) lives in a `.env` file
that is **never committed** to Git. A template is provided.

**Create your `.env`:**

```powershell
# Windows (PowerShell)
Copy-Item .env.example .env
```

```bash
# macOS / Linux
cp .env.example .env
```

**Edit `.env`** and replace the two placeholder values:

1. `DJANGO_SECRET_KEY`: generate one with
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(50))"
   ```
2. `POSTGRES_PASSWORD`: any password you like for your local database.

The placeholders work for a quick local test, but please replace them.

### Variables reference

| Variable | Used by | Purpose | Example |
|----------|---------|---------|---------|
| `DJANGO_SECRET_KEY` | Django | Cryptographic signing key. **Required.** | long random string |
| `DJANGO_DEBUG` | Django | Debug pages. `True` locally only. | `True` |
| `DJANGO_ALLOWED_HOSTS` | Django | Comma-separated host names to serve. | `localhost,127.0.0.1` |
| `DJANGO_TIME_ZONE` | Django | IANA time zone. | `UTC` |
| `POSTGRES_DB` | Docker + Django | Database name. | `interntrack` |
| `POSTGRES_USER` | Docker + Django | Database user. | `interntrack` |
| `POSTGRES_PASSWORD` | Docker + Django | Database password. | (your choice) |
| `POSTGRES_HOST` | Django | Where the DB is. Keep `127.0.0.1` for the Docker setup. | `127.0.0.1` |
| `POSTGRES_PORT` | Docker + Django | Port on your machine. Change if 5432 is taken. | `5432` |
| `POSTGRES_CONNECT_TIMEOUT` | Django | Seconds to wait for a DB connection. | `5` |

The **same `.env` file** is read by both Docker Compose (to create the
database) and Django (to connect to it), so credentials are defined once.

> ⚠️ Set `POSTGRES_PASSWORD` **before** the first `docker compose up`.
> PostgreSQL only applies it when the database volume is first created.
> To change it later, see [Common errors](#password-authentication-failed-for-user-interntrack).

## 6. Start PostgreSQL with Docker

```bash
docker compose up -d --wait
```

- `-d` runs it in the background.
- `--wait` returns only once the database passes its health check.
  The first run downloads the PostgreSQL image (~110 MB).

**Check status:**

```bash
docker compose ps
```

Expected: `STATUS` shows **`(healthy)`**.

| Command | What it does |
|---------|--------------|
| `docker compose up -d --wait` | Start the database |
| `docker compose ps` | Show status |
| `docker compose logs -f db` | Follow database logs (Ctrl+C to exit) |
| `docker compose stop` | Stop, keep data |
| `docker compose down` | Stop and remove container, **keep data** |
| `docker compose down -v` | ⚠️ Stop and **delete all database data** |

Data is stored in a named Docker volume (`postgres_data`), so it survives
restarts. The database port is bound to `127.0.0.1` only, so it is not
exposed to your network.

## 7. Install dependencies and run migrations

**Create and activate a virtual environment** (once per clone):

```powershell
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

Your prompt now starts with `(.venv)`. **Activate it again in every new
terminal** before running `python manage.py ...`.

**Install packages:**

```bash
pip install -r requirements.txt
```

**Apply database migrations:**

```bash
python manage.py migrate
```

Expected: a list of `Applying ... OK` lines (first time) or
`No migrations to apply.`

**(Optional) Create an admin user** for <http://127.0.0.1:8000/admin/>:

```bash
python manage.py createsuperuser
```

## 8. Start the Django server

```bash
python manage.py runserver
```

The server runs at <http://127.0.0.1:8000/> until you press **Ctrl+C**.
To use another port: `python manage.py runserver 8001`.

> Visiting `/` itself shows a 404 page for now. No home page exists yet in
> DT-1. Use `/health/` or `/admin/`.

## 9. Health endpoint

**URL:** <http://127.0.0.1:8000/health/> (method: `GET`)

It runs a real query (`SELECT 1`) against PostgreSQL on every request.

| Situation | HTTP status | Body |
|-----------|-------------|------|
| Django up, database reachable | `200 OK` | `{"status": "ok", "database": "ok"}` |
| Database unreachable | `503 Service Unavailable` | `{"status": "error", "database": "unavailable"}` |

- Responses are marked non-cacheable.
- Error details are written to the server console, never sent to the
  client.
- If the database is down, the response arrives after
  `POSTGRES_CONNECT_TIMEOUT` seconds (default 5).

Check it from the command line:

```powershell
# Windows (PowerShell)
Invoke-RestMethod http://127.0.0.1:8000/health/
```

```bash
# macOS / Linux
curl -i http://127.0.0.1:8000/health/
```

## 10. Running tests

PostgreSQL must be running (`docker compose up -d --wait`) and the virtual
environment active.

```bash
python manage.py test
```

Django creates a temporary `test_interntrack` database, runs the tests, and
deletes it. Expected ending:

```
Ran 7 tests in 0.3s

OK
```

Verbose output: `python manage.py test -v 2`.

The same tests also run automatically on GitHub for every push and pull
request; see [Continuous integration (CI)](#15-continuous-integration-ci).

Other useful checks:

```bash
python manage.py check                          # configuration problems
python manage.py makemigrations --check --dry-run   # forgotten migrations
docker compose config --quiet                   # docker-compose.yml is valid
```

## 11. Common errors and solutions

#### `failed to connect to the docker API ... dockerDesktopLinuxEngine` / `Cannot connect to the Docker daemon`
Docker Desktop is not running. Start it, wait for "Engine running", and retry.

#### `required variable POSTGRES_PASSWORD is missing a value: Set POSTGRES_PASSWORD in .env`
There is no `.env` file, or it lacks that variable. Run
`Copy-Item .env.example .env` (Windows) / `cp .env.example .env`, and run
`docker compose` from the folder containing `.env`.

#### `django.core.exceptions.ImproperlyConfigured: Set the DJANGO_SECRET_KEY environment variable`
Same cause: `.env` is missing or not in the project root. Create it as in
[section 5](#5-environment-configuration).

#### `Bind for 127.0.0.1:5432 failed: port is already allocated` / `ports are not available`
Something else (often a locally installed PostgreSQL) uses port 5432.
Set `POSTGRES_PORT=5433` in `.env`, then `docker compose up -d --wait` again.
Django reads the same variable, so nothing else needs changing.

#### `password authentication failed for user "interntrack"`
`POSTGRES_PASSWORD` in `.env` was changed **after** the database volume was
created. PostgreSQL still has the old password. Either:

- put the old password back in `.env`, **or**
- reset the local database (⚠️ deletes all local data):
  ```bash
  docker compose down -v
  docker compose up -d --wait
  python manage.py migrate
  ```

#### `/health/` returns `503` / `connection refused` / `connection timeout expired`
PostgreSQL is not running or not healthy. Run `docker compose ps`. If it is
not `(healthy)`, run `docker compose up -d --wait` and check
`docker compose logs db`. Also confirm `POSTGRES_HOST` and `POSTGRES_PORT`
in `.env` match the Docker setup (`127.0.0.1`, same port).

#### Every request is slow (~5 seconds) even though the database is up
`POSTGRES_HOST` is set to `localhost`. On Windows this may try IPv6 (`::1`)
first, which Docker does not publish to. Use `POSTGRES_HOST=127.0.0.1`.

#### `.\.venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled on this system`
PowerShell's execution policy blocks the activation script. Run once:
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```
Or use Command Prompt instead: `.venv\Scripts\activate.bat`.

#### `ModuleNotFoundError: No module named 'django'` / `No module named 'environ'`
The virtual environment is not active (no `(.venv)` in the prompt).
Activate it (section 7). If it still fails, rerun `pip install -r requirements.txt`.

#### `'python' is not recognized` (Windows) / `command not found: python` (macOS)
Windows: reinstall Python with "Add python.exe to PATH" ticked, or use `py`
instead of `python`. macOS/Linux: use `python3` to create the venv. Inside
an active venv, `python` works.

#### `DisallowedHost: Invalid HTTP_HOST header`
You are opening the site with a host name not listed in
`DJANGO_ALLOWED_HOSTS`. Add it (comma-separated) in `.env` and restart the server.

#### `Error: That port is already in use.` (runserver)
Another process uses port 8000. Run `python manage.py runserver 8001`, or
stop the other process.

#### Tests fail with `permission denied to create database`
The database user cannot create the test database. With the provided
Docker setup the user is a superuser, so this happens only with a
custom/external PostgreSQL. Grant it with `ALTER USER <user> CREATEDB;`.

## 12. Project structure

```
InternTrack/
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions: run tests on every push / PR
├── apps/                    # InternTrack's own Django apps (one per feature module)
│   └── core/                # Shared infrastructure: health check
│       ├── apps.py
│       ├── health.py        # database_is_available() helper
│       ├── tests.py
│       ├── urls.py          # /health/
│       └── views.py
├── config/                  # Project configuration
│   ├── settings.py          # Settings, all secrets read from .env
│   ├── urls.py              # Root URL routes
│   ├── asgi.py
│   └── wsgi.py
├── .env.example             # Template for your local .env (committed)
├── .env                     # Your local secrets (NOT committed, git-ignored)
├── .gitignore
├── docker-compose.yml       # PostgreSQL service
├── manage.py
├── requirements.txt         # Pinned Python dependencies
└── README.md
```

**Adding a new app** (for later milestones):

```bash
mkdir apps/<name>
python manage.py startapp <name> apps/<name>
```

Then in `apps/<name>/apps.py` set `name = "apps.<name>"`, and add
`"apps.<name>"` to `LOCAL_APPS` in `config/settings.py`.

## 13. Daily workflow cheat sheet

```bash
# start of the day
docker compose up -d --wait
.\.venv\Scripts\Activate.ps1           # macOS/Linux: source .venv/bin/activate
git pull
pip install -r requirements.txt        # in case dependencies changed
python manage.py migrate               # in case migrations changed
python manage.py runserver

# end of the day
# Ctrl+C to stop the server, then:
docker compose stop
```

## 14. Team Git workflow

Every team member has **their own branch**, created from `main`:

| Member | Branch |
|--------|--------|
| Tharun | `tharun` |
| Atul   | `atul` |
| Ritika | `ritika` |
| Kiunal | `kiunal` |

**Rules**

1. Never commit or push directly to `main`.
2. Work and push **only** on your own branch.
3. Get your changes into `main` through a **pull request (PR)**.
4. Wait for a review before merging.

### One-time setup (first time only)

Replace `<your-branch>` with your branch from the table (`tharun`, `atul`,
`ritika` or `kiunal`):

```bash
git clone https://github.com/gundatharuntej2006-hue/InternTrack.git
cd InternTrack
git fetch origin
git switch --track origin/<your-branch>
```

Then follow [Quick start](#quick-start-tldr) from the `Copy-Item` / `cp .env.example .env` step.

Copy-paste version per member:

```bash
# Tharun
git switch --track origin/tharun

# Atul
git switch --track origin/atul

# Ritika
git switch --track origin/ritika

# Kiunal
git switch --track origin/kiunal
```

> Already cloned the repo earlier? Skip `git clone` and just run
> `git fetch origin` followed by your `git switch --track ...` line.

### Every time you start working: bring in the latest `main`

```bash
git switch <your-branch>        # e.g. git switch atul
git fetch origin
git merge origin/main           # bring other members' merged work into your branch
```

If Git reports a **merge conflict**, open the listed files, keep the correct
code, then `git add <file>` and `git commit`. Ask the team if unsure.

### Make changes, commit and push

```bash
git status                      # see what changed
git add <file1> <file2>         # stage specific files (never .env)
git commit -m "Short description of what you did"
git push origin <your-branch>   # e.g. git push origin ritika
```

> Run `git status` before every commit and check that `.env`, `.venv/`
> or other local files are **not** listed. `.gitignore` should already
> exclude them.

### Open a pull request into `main`

**Website:** open
<https://github.com/gundatharuntej2006-hue/InternTrack/pulls>, click
**New pull request**, set **base: `main`** ← **compare: `<your-branch>`**,
describe your change and click **Create pull request**.

**Or with GitHub CLI:**

```bash
gh pr create --base main --head <your-branch> --title "DT-x: what you did" --body "Details, how you tested it"
```

Then **wait for a teammate to review**. Merge only after approval, and
after the **CI** check on the pull request is green (see
[section 15](#15-continuous-integration-ci)).

### After your PR is merged

```bash
git switch <your-branch>
git fetch origin
git merge origin/main           # keep your branch up to date with main
```

### Tip: keep your email private

Commits are public in this repository. To avoid publishing your personal
email, enable **GitHub → Settings → Emails → "Keep my email addresses
private"**, then set your GitHub no-reply address for this repo:

```bash
git config user.email "<id>+<username>@users.noreply.github.com"   # shown on that settings page
```

---

### Security notes

- Never commit `.env` or any real password/secret. `.gitignore` already
  excludes `.env` and `.env.*` (except `.env.example`).
- The values in `.env.example` are placeholders for local development only.
- `DJANGO_DEBUG` must be `False` in any shared or production environment.

---

## 15. Continuous integration (CI)

Every push to **any branch** and every **pull request** automatically runs
the workflow in [`.github/workflows/ci.yml`](.github/workflows/ci.yml) on
GitHub Actions. You can also start it by hand from the **Actions** tab
(**CI → Run workflow**).

What it does, on a fresh Ubuntu runner:

1. Starts a temporary **PostgreSQL 17** container (same image as
   `docker-compose.yml`) and waits until it is healthy.
2. Installs **Python 3.11** and the pinned packages from `requirements.txt`.
3. Runs `python manage.py check`, `python manage.py makemigrations --check --dry-run`
   and `python manage.py test --verbosity 2`.

If any step fails, the check turns red on the commit / pull request. Click
**Details** next to the check to see the log.

**No `.env` and no secrets are needed.** The workflow sets its own
environment variables. The database password in `ci.yml` is a throwaway
value for a database that exists only during that CI run, and
`DJANGO_SECRET_KEY` is randomly generated on every run. Never put real
passwords or keys into the workflow file; if a later milestone needs one,
store it under **Settings → Secrets and variables → Actions** and reference
it as `${{ secrets.NAME }}`.

The workflow has read-only access to the repository, and its actions are
pinned to exact commit SHAs.
