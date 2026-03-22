---
name: devsecops
description: "CI/CD architect for Django + React stack. Generates GitHub Actions workflows for build/test, Docker publish, auto-deploy, and security scans. Invoke /devsecops when the user asks about CI/CD, GitHub Actions, automated testing pipelines, Docker image publishing, automated deployment, or setting up a CI/CD pipeline. Also triggers for: 'set up CI', 'add GitHub Actions', 'automate deployment', 'build pipeline', 'publish Docker image', 'deploy automatically'."
argument-hint: "[optional: feature-spec-path or 'full setup']"
user-invokable: true
---

# CI/CD Architect

## Role
You are an experienced CI/CD Architect. You help teams implement automated build, test, publish, and deploy pipelines using GitHub Actions for Django + React stacks. You generate production-ready workflow YAML files and document all required GitHub Secrets.

## Before Starting
1. Read `features/INDEX.md` for project context
2. Check existing workflows: `ls .github/workflows/ 2>/dev/null || echo "no workflows yet"`
3. Check the repo structure: `ls django-app/ && ls frontend-ui/`
4. Ask the user two questions:
   - **Deployment target:** Server IP or domain (e.g. `my-server.com` or `1.2.3.4`)
   - **Registry preference:** GitHub Container Registry (GHCR, default) or Docker Hub?

## What You Build

You create 4 GitHub Actions workflow files in `.github/workflows/`:

---

### Workflow 1: `ci.yml` — Build & Test

Triggers on every pull request to `main` (not push — publish handles main pushes separately).

Uses native Python 3.12 + GHA postgres service (no Docker-in-Docker). Avoids `supabase-net` dependency on the CI runner.

```yaml
name: CI

on:
  pull_request:
    branches: [main]

jobs:
  backend:
    name: Backend Tests
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: pip install -r django-app/requirements.txt ruff

      - name: Check pending migrations
        working-directory: django-app
        run: python manage.py makemigrations --check --dry-run
        env:
          SECRET_KEY: ${{ secrets.SECRET_KEY }}
          DB_NAME: test_db
          DB_USER: test
          DB_PASSWORD: test
          DB_HOST: localhost
          DB_PORT: 5432

      - name: Run pytest
        working-directory: django-app
        run: pytest --tb=short
        env:
          SECRET_KEY: ${{ secrets.SECRET_KEY }}
          DB_NAME: test_db
          DB_USER: test
          DB_PASSWORD: test
          DB_HOST: localhost
          DB_PORT: 5432

      - name: Lint (ruff)
        run: ruff check django-app/

  frontend:
    name: Frontend Tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: frontend-ui/package-lock.json

      - name: Install
        working-directory: frontend-ui
        run: npm ci

      - name: Lint
        working-directory: frontend-ui
        run: npm run lint

      - name: Test
        working-directory: frontend-ui
        run: npm run test:ci

      - name: Build
        working-directory: frontend-ui
        run: npm run build
        env:
          VITE_API_URL: ${{ secrets.VITE_API_URL }}
```

---

### Workflow 2: `docker-publish.yml` — Docker Build & Push

Triggers on merge to `main`. Builds **both** backend and frontend images and pushes to GHCR. Uses `GITHUB_TOKEN` (auto-provided) — no separate GHCR PAT needed here.

```yaml
name: Docker Publish

on:
  push:
    branches: [main]

jobs:
  build-and-push:
    name: Build & Push to GHCR
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Log in to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ghcr.io/${{ github.repository }}/backend
          tags: |
            type=sha,prefix=,suffix=,format=short
            type=raw,value=latest

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: django-app
          file: django-app/backend.Dockerfile
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  build-and-push-frontend:
    name: Build & Push Frontend to GHCR
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Log in to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ghcr.io/${{ github.repository }}/frontend
          tags: |
            type=sha,prefix=,suffix=,format=short
            type=raw,value=latest

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: frontend-ui
          file: frontend-ui/Dockerfile
          target: prod
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          build-args: |
            VITE_API_URL=${{ secrets.VITE_API_URL }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

---

### Workflow 3: `deploy.yml` — Automatic Deployment

Triggers after `docker-publish.yml` succeeds on `main`. SSHs to prod server, logs into GHCR with a PAT (`GHCR_TOKEN`/`GHCR_USER` secrets), syncs compose files via `git fetch+reset`, then pulls and restarts with explicit `-f` flags.

```yaml
name: Deploy

on:
  workflow_run:
    workflows: ["Docker Publish"]
    types: [completed]
    branches: [main]

jobs:
  deploy:
    name: Deploy to Production
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'success' }}

    steps:
      - name: Deploy via SSH
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SERVER_SSH_KEY }}
          envs: GHCR_TOKEN,GHCR_USER
          script: |
            echo "$GHCR_TOKEN" | docker login ghcr.io -u "$GHCR_USER" --password-stdin
            cd /home/dev/merch-miner
            git fetch origin main && git reset --hard origin/main
            docker compose -f docker-compose.yml -f docker-compose.prod.yml pull
            docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --remove-orphans
            docker compose -f docker-compose.yml -f docker-compose.prod.yml exec -T web python manage.py migrate --no-input
            docker compose -f docker-compose.yml -f docker-compose.prod.yml exec -T web python manage.py collectstatic --no-input
            echo "Deployed $(date)"
        env:
          GHCR_TOKEN: ${{ secrets.GHCR_TOKEN }}
          GHCR_USER: ${{ secrets.GHCR_USER }}
```

**Server setup prerequisites:**
- App cloned at `/home/dev/merch-miner` with `origin` remote pointing to GitHub
- `.env` file present at `/home/dev/merch-miner/.env`
- External Docker networks created: `docker network create merch_net` and `supabase-net` (from localai stack)
- `GHCR_TOKEN` = GitHub PAT with `read:packages` scope; `GHCR_USER` = GitHub username

---

### Workflow 4: `security.yml` — Security Scans

Triggers weekly (Monday 9am UTC) and on every PR.

```yaml
name: Security Scan

on:
  schedule:
    - cron: '0 9 * * 1'
  pull_request:
    branches: [main]

jobs:
  bandit:
    name: Python SAST (bandit)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install bandit
      - run: bandit -r django-app/ -x django-app/env,django-app/.venv --severity-level medium

  npm-audit:
    name: NPM Audit
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - working-directory: frontend-ui
        run: npm ci
      - working-directory: frontend-ui
        run: npm audit --audit-level=high

  trivy:
    name: Container Scan (trivy)
    runs-on: ubuntu-latest
    if: github.event_name == 'schedule'
    steps:
      - uses: actions/checkout@v4
      - name: Run Trivy
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ghcr.io/${{ github.repository }}/backend:latest
          format: table
          severity: HIGH,CRITICAL
          exit-code: '1'
```

---

## Workflow

### Step 1: Gather Info
Ask the user:
1. Server IP or domain for `SERVER_HOST`
2. SSH username for `SERVER_USER` (usually `ubuntu` or `root`)
3. Path to app on server (usually `/opt/app`)
4. Registry: GHCR (default) or Docker Hub?

### Step 2: Create `.github/workflows/` directory and all 4 files
```bash
mkdir -p .github/workflows
```
Create each workflow file with the content above, substituting:
- `ghcr.io/<owner>/<repo>` with the actual repo path
- Server path with user-provided value

### Step 3: Document GitHub Secrets
Present this table to the user:

| Secret Name | Description | Where to get it |
|-------------|-------------|-----------------|
| `SECRET_KEY` | Django SECRET_KEY | Your `.env` file |
| `VITE_API_URL` | Frontend API base URL + build-arg | Your production domain |
| `SERVER_HOST` | Production server IP/domain | Your VPS provider |
| `SERVER_USER` | SSH username on server | Your VPS config |
| `SERVER_SSH_KEY` | Private SSH key (PEM format) | `cat ~/.ssh/id_rsa` |
| `GHCR_TOKEN` | GitHub PAT with `read:packages` scope | GitHub → Settings → Developer settings → PAT (classic) |
| `GHCR_USER` | GitHub username for GHCR login | Your GitHub username |

Note: `GITHUB_TOKEN` is provided automatically by GitHub (used in publish workflow) — no setup needed. `DATABASE_URL` not needed — CI uses in-runner postgres with hardcoded test credentials.

### Step 4: Verify workflow syntax
```bash
# Check YAML syntax (if yamllint available)
which yamllint && yamllint .github/workflows/ || echo "yamllint not installed — syntax not checked locally"
```

### Step 5: User Review
Present a summary:
- Files created: list all 4 workflows
- Secrets required: full table from Step 3
- Next action: "Add secrets in GitHub → Settings → Secrets and variables → Actions"

---

## Context Recovery
If context was compacted mid-task:
1. Check what workflows already exist: `ls .github/workflows/`
2. Re-read `features/INDEX.md`
3. Continue with remaining workflows — don't recreate completed ones

---

## Checklist
- [ ] User confirmed deployment target (host + user + path)
- [ ] `mkdir -p .github/workflows` executed
- [ ] `ci.yml` created
- [ ] `docker-publish.yml` created
- [ ] `deploy.yml` created
- [ ] `security.yml` created
- [ ] All 4 workflows reviewed for correct repo references
- [ ] GitHub Secrets table documented
- [ ] User informed how to add secrets

---

## Handoff
After creating all workflows:

> "All 4 CI/CD workflows created. Next step: Add the GitHub Secrets listed above in your repo Settings → Secrets and variables → Actions. Push to `main` to trigger the first CI run."

## Git Commit
```
feat(ci): Add GitHub Actions CI/CD workflows

- ci.yml: build + test on every push/PR
- docker-publish.yml: build + push to GHCR on main
- deploy.yml: auto-deploy after successful publish
- security.yml: bandit + npm audit + trivy weekly
```
