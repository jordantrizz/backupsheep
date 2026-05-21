
# BackupSheep

Automating backups is costly and takes time. With BackupSheep, you can quickly automate server snapshots and offsite backups without writing code.

## Databases (offsite backups)

Automate the backup process for your various databases like MySQL, PostgreSQL,
MongoDB, and more. Our sophisticated retention policies enable you to retain any
number of daily, weekly, or monthly backups as required.

 1. MySQL
 2. MariaDB
 3. PostgreSQL

## Websites/Servers (offsite backups)

Set up automatic backups of your files from any Linux-based operating system. With
our sophisticated retention policies, you can maintain as many daily, weekly, or
monthly backups as necessary.

 1. FTP
 2. FTPS
 3. sFTP
 4. SSH

## Cloud Services (server snapshots)

Automate periodic snapshots of your servers. Maintain any number of daily, weekly,
or monthly backups you need with our rotation retention policies. We are compatible  
with all major cloud service providers.

 1. AWS
 2. DigitalOcean
 3. Google Cloud
 4. Hetzner
 5. Linode
 6. Oracle
 7. UpCloud
 8. Vultr

## SaaS Backups (offsite backups)

BackupSheep provides plugins and API integrations to secure your CMS and SaaS
applications. This allows for the effortless safeguarding of your critical data.
These tools are designed to seamlessly integrate with your existing systems,
enabling easy and regular backups. Hence, you can rest easy knowing your valuable  
data is well-protected.

 1. Basecamp
 2. WordPress

## Storage Integrations (for offsite backups)

Connect your cloud storage providers and store backups in multiple storage accounts simultaneously.

 1. AWS S3
 2. Alibaba Cloud
 3. Azure
 4. BackBlaze B2
 5. Cloudflare R2
 6. DigitalOcean Spaces
 7. Dropbox
 8. ExoScale
 9. Filebase
 10. Google Cloud
 11. Google Drive
 12. IBM Cloud
 13. iDrive
 14. IONOS
 15. Levila
 16. Linode
 17. OneDrive
 18. Oracle
 19. pCloud
 20. RackCorp
 21. Scaleway
 22. Tencent
 23. UpCloud
 24. Vultr
 25. Wasabi

## Notice

This is a complete rewrite of the BackupSheep application. The repository can be bootstrapped locally, but feature coverage and operational documentation are still incomplete while the rewrite continues. Please follow the repository for updates.

## Technology Stack

Django, PostgreSQL, AlpineJS and TailwindCSS.

## Installation

BackupSheep currently supports two installation paths:

- Native setup for local development with Django's development server
- Docker setup for a containerized runtime using the repository's existing Dockerfiles

Both methods require PostgreSQL 14.x and a configured `.env` file.

### Method 1: Native

### Native prerequisites

- Python 3.12
- PostgreSQL 14.x
- `pip` and `venv`

### Native step 1: Clone the repository

```bash
git clone https://github.com/bilal414/backupsheep.git
cd backupsheep
```

### Native step 2: Create a virtual environment

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

### Native step 3: Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Native step 4: Create a PostgreSQL database

Create an empty PostgreSQL 14.x database and a user with permission to manage it. You will add those values to `.env` in the next step.

### Native step 5: Configure environment variables

```bash
cp .env_sample .env
```

At minimum, set these values in `.env`:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_SERVER`
- `APP_DOMAIN`
- `APP_PROTOCOL`
- `APP_NAME`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`

Most third-party integration credentials in `.env_sample` are optional for a basic local bootstrapping workflow.

### Native step 6: Initialize the database

```bash
python manage.py migrate
python manage.py createcachetable
```

The cache table is required because the default cache backend is database-backed.

### Native step 7: Collect static assets

```bash
python manage.py collectstatic --noinput
```

### Native step 8: Start the application

```bash
python manage.py runserver 0.0.0.0:8000
```

Open `http://localhost:8000` after the server starts.

### Runtime notes

- Local development uses Django's built-in server.
- The repository includes Celery, `django-celery-beat`, and `django-celery-results`, but no committed local broker configuration is documented yet.

### Method 2: Docker

Use this path if you want to run the app in the same production-style shape used by the repository's container entrypoints.

#### Docker prerequisites

- Docker
- PostgreSQL 14.x running outside the container, or another reachable PostgreSQL instance
- A configured `.env` file in the repository root

#### Docker step 1: Clone the repository

```bash
git clone https://github.com/bilal414/backupsheep.git
cd backupsheep
```

#### Docker step 2: Configure environment variables

```bash
cp .env_sample .env
```

Set the same minimum values required for the native setup, especially the PostgreSQL connection values:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_SERVER`
- `APP_DOMAIN`
- `APP_PROTOCOL`
- `APP_NAME`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`

Point `DB_HOST` at a PostgreSQL server reachable from the container.

#### Docker step 3: Build the base image

The application image depends on a local `backupsheep-base` image defined by `DockerfileBase`.

```bash
docker build -f DockerfileBase -t backupsheep-base .
```

#### Docker step 4: Build the application image

```bash
docker build -t backupsheep .
```

#### Docker step 5: Run the container

```bash
docker run --env-file .env -p 8000:80 backupsheep
```

The container entrypoint starts Nginx, runs `collectstatic`, applies migrations, and launches Gunicorn automatically.

Open `http://localhost:8000` after the container starts.

#### Docker notes

- The repo does not currently include a committed `docker-compose.yml` for wiring the app and PostgreSQL together.
- The Docker path is best suited for runtime validation. The native path remains the better contributor workflow.

## Development

### Local architecture

This project is a Django monolith with two primary surfaces:

- Console routes under `apps.console`
- API routes under `apps.api.v1`

Key locations:

- `backupsheep/settings.py` for environment-driven settings, database config, static files, and installed apps
- `backupsheep/urls.py` for root routing
- `backupsheep/celery.py` for Celery bootstrap
- `apps/_migrations/` for the custom migration module used by the `apps` Django app
- `apps/_tasks/integration/` for provider-specific backup and storage integrations
- `apps/console/_templates/` and `apps/console/_static/` for the server-rendered UI

### Validation

Useful commands while developing locally:

```bash
python manage.py check
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py test <app_or_module>
```

There does not appear to be a committed full test suite yet, so prefer targeted Django tests for the area you are changing.

### Background jobs and scheduling

Scheduling and job state are part of the application, and the repo includes Celery-related packages plus `django-celery-beat` models. However, the repository does not currently document a local broker or worker startup flow. If you are developing scheduling or async task features, expect to provide your own broker configuration until that setup is documented in-repo.

### Container/runtime context

The container entrypoints run a production-style sequence:

```bash
python manage.py collectstatic --noinput
python manage.py migrate
gunicorn backupsheep.wsgi:application --workers=4 --timeout=3600
```

That path is useful for deployment-oriented testing, but the recommended contributor workflow is still the local Django setup above.

## Repository Map with Repomix

This repository can generate a repo map for high-level AI/code-review workflows using `repomix`.

This repository also uses codemaps for faster targeted code navigation. Generated codemaps live in `.codemaps/`, with the current repository map at `.codemaps/backupsheep.codemap.md`.

Important: `.repomap-snapshot.md` can become extremely large, to the point of consuming millions of tokens. Treat it as a temporary, high-level artifact for extracting core features and repository structure, not as routine context to attach to every prompt.

In practice, this file should usually be generated once, used to help update high-level repository guidance such as `AGENTS.md`, and then left out of normal workflows. The snapshot is gitignored for that reason.

Install it globally if needed:

```bash
npm install -g repomix
```

Generate a lightweight repository snapshot with directory structure and metadata only:

```bash
repomix --no-files --style markdown --output .repomap-snapshot.md
```

Generate a richer structural map that compresses source files into high-level symbols such as classes and functions:

```bash
repomix --compress --style markdown --output .repomap-snapshot.md
```

Generate the codemap used by this repository:

```bash
mkdir -p .codemaps && repomix --compress --style markdown --output .codemaps/backupsheep.codemap.md
```

Useful options for this repo:

- `--include-full-directory-structure` to force the full tree into the output.
- `--token-count-tree` to inspect which folders/files dominate the context window.
- `--no-git-sort-by-changes` if you want a stable alphabetical tree instead of git-weighted ordering.

If you explicitly need to refresh the repository summary, open `.repomap-snapshot.md`, extract the core structure and features you need, and fold that summary back into `AGENTS.md` instead of repeatedly sharing the full snapshot.

## Background

BackupSheep was a paid SaaS application from 2017 to 2023, serving over 6,500 users at its peak. Unfortunately, a poor decision to offer a lifetime deal (LTD) through AppSumo without proper due diligence led to a decline.
As a result, BackupSheep was shut down in 2023. Rather than letting years of development go to waste, I have decided to open source BackupSheep.
