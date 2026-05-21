
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

Both methods support multiple runtime tiers. Native setup still expects a configured `.env` file, while the included Docker Compose files provide local defaults.

Available tiers:

- `lite`: SQLite, local memory cache, no external broker
- `standard`: PostgreSQL, local memory cache, no external broker
- `full`: PostgreSQL, RabbitMQ, web plus worker/beat processes

### Method 1: Native

### Native prerequisites

- Python 3.12
- SQLite for `lite` mode, or PostgreSQL 14.x for `standard`/`full`
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

### Native step 4: Choose a runtime tier

For the fastest local boot, use `lite` mode with SQLite and local memory cache. For PostgreSQL-backed local parity, use `standard`.

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

For `lite`, also set:

- `APP_TIER=lite`
- `APP_DB_BACKEND=sqlite`
- `APP_CACHE_BACKEND=locmem`

For PostgreSQL-backed modes, also set:

- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`

Most third-party integration credentials in `.env_sample` are optional for a basic local bootstrapping workflow.

### Native step 6: Initialize the database

```bash
python manage.py migrate
```

If you use the database cache backend, also run:

```bash
python manage.py createcachetable
```

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
- `lite` mode defaults to SQLite and local memory cache so it can boot without external services.
- The repository includes Celery, `django-celery-beat`, and `django-celery-results`. In non-worker modes, tasks can fall back to eager execution.

### Method 2: Docker

Use this path if you want to run the app in a tiered containerized setup.

#### Docker prerequisites

- Docker

#### Docker step 1: Clone the repository

```bash
git clone https://github.com/bilal414/backupsheep.git
cd backupsheep
```

#### Docker step 2: Choose a Compose file

- `docker-compose.lite.yml`: single-container SQLite deployment for homelab and fast boot
- `docker-compose.standard.yml`: PostgreSQL-backed app container
- `docker-compose.full.yml`: PostgreSQL, RabbitMQ, web, worker, and beat
- `docker-compose.yml`: the default PostgreSQL-backed standard setup

#### Docker step 3: Build the application image

The included Compose files now supply minimum local settings for you, so you can build and run the stack without creating a `.env` file first.

If you want to override those defaults, either edit the selected Compose file or provide environment variables when you run the container manually.

Using Docker Compose:

```bash
docker compose -f docker-compose.lite.yml build app
```

Or build manually:

```bash
docker build -t backupsheep .
```

#### Docker step 4: Run the selected tier

Lite tier:

```bash
docker compose -f docker-compose.lite.yml up --build
```

Standard tier:

```bash
docker compose -f docker-compose.standard.yml up --build
```

Full tier:

```bash
docker compose -f docker-compose.full.yml up --build
```

The default Compose file continues to point at the standard PostgreSQL-backed setup:

```bash
docker compose up --build
```

Or run the app container manually:

```bash
docker run -p 8000:80 \
  -e DJANGO_SERVER=dev \
  -e DJANGO_DEBUG=true \
  -e DJANGO_ALLOWED_HOSTS='*' \
  -e DJANGO_SECRET_KEY=change-this-key \
  -e APP_DOMAIN=localhost:8000 \
  -e APP_PROTOCOL=http:// \
  -e APP_NAME=BackupSheep \
  -e APP_TIER=standard \
  -e APP_DB_BACKEND=postgres \
  -e APP_CACHE_BACKEND=locmem \
  -e DB_NAME=backupsheep \
  -e DB_USER=backupsheep \
  -e DB_PASSWORD=backupsheep \
  -e DB_HOST=host.docker.internal \
  -e DB_PORT=5432 \
  backupsheep
```

The container entrypoint starts Nginx, runs `collectstatic`, applies migrations, and launches Gunicorn automatically.

Open `http://localhost:8000` after the container starts.

#### Docker notes

- The tiered Compose files live at `docker-compose.lite.yml`, `docker-compose.standard.yml`, and `docker-compose.full.yml`.
- The Compose files do not require a repository-root `.env` file for local boot.
- `lite` is the fastest boot path and does not require any external service containers.
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
