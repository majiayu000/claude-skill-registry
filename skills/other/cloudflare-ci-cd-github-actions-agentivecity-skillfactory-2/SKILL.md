---
name: "cloudflare-ci-cd-github-actions"
description: "Use this skill whenever the user wants to set up, refactor, or maintain a GitHub Actions CI/CD pipeline for deploying Cloudflare Workers/Pages apps (e.g. Hono + TypeScript) with D1/R2, including tests, build, migrations, and multi-environment deploys."
---

# Cloudflare CI/CD with GitHub Actions Skill

## Purpose

You are a specialized assistant for **automating deployment of Cloudflare Workers/Pages apps**
using **GitHub Actions**.

Use this skill to:

- Create or refactor **GitHub Actions workflows** for:
  - Testing & linting
  - Building the Worker
  - Running D1 migrations (via Wrangler)
  - Deploying to Cloudflare **dev/staging/production**
- Wire **Cloudflare API tokens** and secrets into GitHub Actions
- Coordinate **deploy + DB migrations** safely
- Support **preview deployments** for feature branches (optional)
- Keep pipelines **fast, reliable, and readable**

Do **not** use this skill for:

- Local-only workflows without GitHub
- GitLab/Bitbucket CI (different skill)
- Deep Cloudflare app architecture (handled by Hono/Workers skills)

If `CLAUDE.md` describes CI/CD standards (job naming, env naming, required checks), follow them.

---

## When To Apply This Skill

Trigger this skill when the user says things like:

- “Set up GitHub Actions to deploy my Cloudflare Worker.”
- “Run tests and deploy to production on merge to main.”
- “Deploy staging on every PR with a preview URL.”
- “Wire Cloudflare token into GitHub Actions securely.”
- “Add D1 migrations into the CI/CD pipeline.”
- “Refactor my messy Actions workflow for Cloudflare.”

Avoid when:

- CI/CD is managed by another system and GitHub Actions is not used.
- Only local/manual deployment is expected.

---

## Required Inputs & Secrets

This skill expects the following GitHub repo secrets (names can be customized):

- `CLOUDFLARE_API_TOKEN` – API Token with appropriate permissions for Workers & D1/R2
- `CLOUDFLARE_ACCOUNT_ID` – Cloudflare account ID
- Optionally environment-specific:

  - `CLOUDFLARE_API_TOKEN_STAGING`
  - `CLOUDFLARE_API_TOKEN_PRODUCTION`

These secrets are configured in **GitHub → Settings → Secrets and variables → Actions**.

Within workflows, they are accessed via `${{ secrets.CLOUDFLARE_API_TOKEN }}` etc.

---

## Basic Workflow Structure

The skill generally recommends at least **two workflows**:

1. **`ci.yml`** – Tests & checks (PRs, pushes).
2. **`deploy.yml`** – Build + deploy (staging/prod) on specific branches or tags.

### 1. CI Workflow (Tests + Lint Only)

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm install

      - name: Lint
        run: npm run lint --if-present

      - name: Test
        run: npm test --if-present
```

This skill can adapt `npm` → `pnpm`/`yarn` based on lockfiles.

### 2. Deploy Workflow (Staging & Production)

```yaml
# .github/workflows/deploy.yml
name: Deploy to Cloudflare

on:
  push:
    branches:
      - main        # production deploy
      - develop     # staging deploy

jobs:
  deploy:
    runs-on: ubuntu-latest

    env:
      CLOUDFLARE_ACCOUNT_ID: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm install

      - name: Install Wrangler
        run: npm install -g wrangler

      - name: Determine environment
        id: env
        run: |
          if [[ "${GITHUB_REF##*/}" == "main" ]]; then
            echo "env_name=production" >> "$GITHUB_OUTPUT"
          else
            echo "env_name=staging" >> "$GITHUB_OUTPUT"
          fi

      - name: Deploy with Wrangler
        env:
          CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
        run: |
          if [ "${{ steps.env.outputs.env_name }}" = "production" ]; then
            wrangler deploy --env production
          else
            wrangler deploy --env staging
          fi
```

This is a **baseline**; this skill will customize it with migrations, R2, etc., per project.

---

## Integrating D1 Migrations in CI/CD

When `cloudflare-d1-migrations-and-production-seeding` is present, this skill will:

- Ensure **migrations run before deploy** (or as part of deploy).
- Keep commands in sync with `wrangler.toml` and DB names.

Example augmented snippet:

```yaml
      - name: Run D1 migrations
        env:
          CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
        run: |
          if [ "${{ steps.env.outputs.env_name }}" = "production" ]; then
            wrangler d1 migrations apply my_db_prod --env production
          else
            wrangler d1 migrations apply my_db_staging --env staging
          fi
```

Ordering options:

1. **Migrations then deploy** (recommended).
2. Combine `wrangler deploy` with integrated migrations if using more advanced patterns.

This skill should:

- Warn about **destructive migrations** against prod.
- Encourage running migrations on a staging DB first and verifying.

---

## Preview Deployments for Pull Requests (Optional)

For feature branches & PRs, this skill can set up **preview Workers**:

- One option: use `wrangler deploy --name my-app-pr-${{ github.event.number }}`.
- Or use **Preview Environments** with ephemeral routes.

Example preview workflow:

```yaml
# .github/workflows/preview.yml
name: Preview Deploy

on:
  pull_request:

jobs:
  preview:
    runs-on: ubuntu-latest
    env:
      CLOUDFLARE_ACCOUNT_ID: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - run: npm install

      - run: npm install -g wrangler

      - name: Deploy Preview
        env:
          CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
        run: |
          wrangler deploy             --name "my-hono-api-pr-${{ github.event.number }}"             --var "NODE_ENV:preview"
```

This skill will:

- Suggest naming conventions for preview workers.
- Optionally comment the preview URL back to the PR (using Actions’ `github-script` or similar).

---

## Caching & Performance in CI

This skill configures caching to make CI faster:

- Node modules cache (via `actions/setup-node` with `cache`).
- If using `pnpm`:

  ```yaml
  - uses: pnpm/action-setup@v4
    with:
      version: 9
      run_install: false

  - uses: actions/cache@v4
    with:
      path: ~/.pnpm-store
      key: ${{ runner.os }}-pnpm-${{ hashFiles('pnpm-lock.yaml') }}
      restore-keys: |
        ${{ runner.os }}-pnpm-
  ```

- For `pnpm install` instead of `npm install`.

This skill will auto-detect package manager based on lockfile names in the repo, when context permits.

---

## Environments & Permissions Model

This skill helps design environment mapping:

- `develop` branch → `staging` environment in `wrangler.toml`
- `main` branch → `production` environment

Optionally:

- `feature/*` branches → preview Worker instances

Permissions & tokens:

- Single `CLOUDFLARE_API_TOKEN` with scoped permissions for all envs, or
- Env-specific tokens, e.g.:
  - `CLOUDFLARE_API_TOKEN_STAGING`
  - `CLOUDFLARE_API_TOKEN_PRODUCTION`

Then choose inside the workflow:

```yaml
      - name: Select API token
        id: token
        run: |
          if [[ "${GITHUB_REF##*/}" == "main" ]]; then
            echo "value=${{ secrets.CLOUDFLARE_API_TOKEN_PRODUCTION }}" >> "$GITHUB_OUTPUT"
          else
            echo "value=${{ secrets.CLOUDFLARE_API_TOKEN_STAGING }}" >> "$GITHUB_OUTPUT"
          fi
```

Then export as `CLOUDFLARE_API_TOKEN` for Wrangler.

---

## Failure Modes & Rollback Strategy

This skill will guide around:

- Tests & lint must pass before deploy job runs.
- If migrations fail:
  - Stop deployment.
  - Inspect logs, fix migration, re-run.
- For rollback:
  - For Workers, deploy the last known good version (`wrangler deploy --tag <release-tag>` when tags are used).
  - For schema-breaking migrations, recommend **forward fixes** rather than trying to downgrade D1 manually (unless very early in lifecycle).

It can also suggest tagging releases in Git (`v1.2.3`) and tying deploys to tags.

---

## Security & Secrets Handling

This skill should ensure:

- No API tokens are echoed or logged.
- No credentials are committed to the repo.
- Only GitHub Secrets are used for tokens/IDs.

It can suggest:

- Restricting `deploy` workflow to protected branches (`main`, `release/*`).
- Requiring PR approvals + passing CI before merging into `main`.

---

## Integration With Other Skills

- `cloudflare-worker-deployment`:
  - This skill uses that skill’s `wrangler.toml` and env naming.
- `cloudflare-d1-migrations-and-production-seeding`:
  - Hooks migration commands into CI/CD.
- `cloudflare-r2-bucket-management-and-access`:
  - R2 is configured in `wrangler.toml`; CI/CD ensures deployments target correct env.
- `hono-app-scaffold`, `hono-d1-integration`, `hono-r2-integration`:
  - CI/CD pipelines run tests that hit these features and then deploy.

---

## Example Prompts That Should Use This Skill

- “Create CI + deploy GitHub Actions for my Hono Worker on Cloudflare.”
- “Run tests and then deploy to staging on every push to develop.”
- “Deploy to production only on main, with D1 migrations included.”
- “Set up preview Workers for PRs with unique names.”
- “Refactor my existing GitHub Actions for Cloudflare into something clean and modular.”

For such tasks, rely on this skill to build a **clean, robust GitHub Actions pipeline** that automates
testing, building, migrating, and deploying your Cloudflare Workers/Pages-based apps.
