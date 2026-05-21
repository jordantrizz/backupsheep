# BackupSheep Copilot Instructions

## Development

* Always create a git commit message for each change made, use the format feat, fix, docs, style, refactor, perf, test, chore and print it out after each time agent chagnes any files.

## Tech stack

* Python 3 with Django 5.x as the main application framework.
* Django REST Framework for JSON APIs under `apps/api/v1`.
* PostgreSQL as the primary app database.
* Celery is present for background work and task autodiscovery.
* Gunicorn + Nginx are used for container/runtime serving.
* Frontend is mostly server-rendered Django templates with static assets in `apps/console/_static`; README also calls out Alpine.js and TailwindCSS.

## Architecture overview

* This is a Django monolith, not a microservice repo.
* `backupsheep/` contains project settings, root URLs, ASGI/WSGI, and Celery bootstrap.
* `apps/` is the main domain package. It holds models, API endpoints, console UI modules, migrations, and provider/task integrations.
* Root routing splits into two surfaces: console routes from `apps.console.urls` and API routes from `apps.api.urls`.
* `apps/api/v1/` is organized by domain area (`account`, `backup`, `storage`, `node`, `website`, etc.), usually with `views.py`, `serializers.py`, `permissions.py`, `filters.py`, and `urls.py`.
* `apps/_tasks/integration/` contains provider-specific backup, cloud, website, and storage integration logic. Prefer extending an existing provider pattern instead of inventing a new abstraction.
* `apps/console/` contains the authenticated web console, templates, and per-domain UI modules.

## Important locations

* `manage.py`: Django entrypoint.
* `backupsheep/settings.py`: env-driven settings, installed apps, DRF config, database config, middleware, static files.
* `backupsheep/urls.py`: root URL composition.
* `backupsheep/celery.py`: Celery app setup.
* `apps/models.py`: top-level model re-export; actual model groups live under `apps/console/*/models.py`.
* `apps/_migrations/`: custom migration module for the `apps` Django app.
* `apps/api/v1/`: REST API implementation.
* `apps/console/_templates/` and `apps/console/_static/`: HTML and static assets.
* `.codemaps/`: repository code maps for fast codebase navigation and context gathering.
* `.env_sample`: expected environment variables.
* `Dockerfile`, `init.sh`, `startup.sh`: container/bootstrap commands.

## Conventions

* Keep changes local to the relevant domain area. If you touch a backup provider, follow the neighboring provider module layout.
* Reuse existing DRF patterns: queryset scoping by current account/member, serializer method fields for display values, dedicated permissions/filter classes, and per-domain `urls.py` registration.
* Keep environment-dependent values in settings or env vars; do not hardcode secrets, hosts, bucket names, or credentials.
* Respect the existing migration setup: new model changes for `apps` belong in `apps/_migrations/`.
* Prefer extending current models/views/serializers over adding parallel copies or one-off helper layers.
* Preserve the current URL split: console pages at the console/auth modules, API endpoints under `/api/`.

## Build and validation commands

* Install deps: `pip install -r requirements.txt`
* Local env: copy `.env_sample` to `.env` and fill required values, especially PostgreSQL settings.
* Migrate DB: `python manage.py migrate`
* Collect static: `python manage.py collectstatic --noinput`
* Run dev server: `python manage.py runserver 0.0.0.0:8000`
* Production-style app server: `gunicorn backupsheep.wsgi:application --workers=4 --timeout=3600`
* Cheap validation: `python manage.py check`
* Tests: no committed automated test suite was found. If you add tests, prefer targeted Django tests and run `python manage.py test <app_or_module>`.

## Patterns and anti-patterns for AI agents

* Do follow existing per-provider folder structure and naming when adding integrations.
* Do keep API changes aligned across `urls.py`, `views.py`, `serializers.py`, `permissions.py`, and `filters.py` when that pattern already exists.
* Do scope data access to the authenticated member/account; avoid broad unfiltered querysets.
* Do make small, surgical edits. This repo has many repeated provider modules, so broad refactors carry high regression risk.
* Do not introduce a new framework, service layer, or generic abstraction unless the existing code clearly uses it.
* Do not move migrations back to default app locations or rename large provider trees casually.
* Do not assume a frontend SPA build pipeline exists.
* Do not assume tests, linters, or typecheckers are already wired up; verify with Django checks and the narrowest executable command available.
