---
name: servd
description: "Servd (servd.host) — Craft-specialised managed hosting for Craft CMS. Covers git push-to-deploy with the optional servd.yaml build config, local → staging → production environments with uni-directional Project Config sync, the servd/craft-asset-storage plugin (S3-backed Flysystem volumes on the svdcdn.com CDN, off-server image transforms, Imager-X/ImageOptimize integrations), Servd's static caching (full vs tag-based purge, {% dynamicInclude %}, CSRF injection, cache-busting) and running Blitz alongside it in reverse-proxy mode, MariaDB/MySQL databases over an SSH tunnel, automatic + manual backups, the Dedicated Queue Runner, environment variables and secrets, the ephemeral load-balanced filesystem (Redis + remote volumes for runtime files), plugin/feature constraints, and Servd-vs-Craft-Cloud differences. Triggers on: servd.yaml, servd/craft-asset-storage, servd-asset-storage plugin handle, SERVD_PROJECT_SLUG, SERVD_SECURITY_KEY, SERVD_BUNDLE_HASH, files.svdcdn.com, Servd static caching, {% dynamicInclude %} (Servd), servd-asset-storage/clone, servd-asset-storage/local/pull-database, push-assets, clear-caches/servd-static-cache, clear-caches/servd-edge-caches, Dedicated Queue Runner, Servd Asset Platform, deploy to Servd, host Craft on Servd, Servd vs Craft Cloud. Do NOT trigger for Craft Cloud (use the craft-cloud skill), generic Craft deployment on Forge/bare metal (craftcms/deployment.md), or general DDEV local dev unrelated to Servd parity (ddev)."
---

# Servd — Managed Hosting for Craft CMS

Reference for Servd (servd.host), a Craft-specialised managed hosting platform. Covers git push-to-deploy and the `servd.yaml` build config, the local → staging → production workflow, the `servd/craft-asset-storage` plugin, Servd's static caching (and running Blitz alongside it), databases over SSH, backups, the queue runner, the ephemeral filesystem, and how Servd differs from Craft Cloud.

This skill is scoped to **Servd specifically** — what's different on Servd vs running Craft yourself on Forge or bare metal, and vs Pixel & Tonic's Craft Cloud. For generic Craft deployment, see the `craftcms` skill's `deployment.md`. For Craft Cloud, see the `craft-cloud` skill.

## Companion Skills — Load When Needed

- **`craftcms`** — When the Servd topic intersects plugin or module PHP (ephemeral-filesystem guards, queue-job design, asset filesystem code).
- **`craft-site`** — When Servd intersects front-end templating (`{% dynamicInclude %}` islands in cached pages, transform usage, CSRF in cached forms).
- **`ddev`** — For local development; Servd has no first-party local environment, so DDEV is the standard local stack.
- **`craft-php-guidelines`** — When editing plugin PHP to add ephemeral-filesystem checks.

## Documentation

Authoritative sources used to write this skill (Servd's own docs):

- Docs landing: https://servd.host/docs
- The Servd workflow: https://servd.host/docs/the-servd-workflow
- Node build step (servd.yaml): https://servd.host/docs/node-build-step
- Asset volumes & filesystems: https://servd.host/docs/servd-asset-volumes-and-filesystems
- Installing the plugin: https://servd.host/docs/installing-the-servd-plugin
- Static caching: https://servd.host/docs/static-caching
- Caching with Blitz: https://servd.host/docs/caching-with-blitz
- Handling runtime-created files: https://servd.host/docs/handling-runtime-created-files
- Dedicated queue runner: https://servd.host/docs/dedicated-queue-runner
- Backup & restore: https://servd.host/docs/backup-restore
- Plugin console commands: https://servd.host/docs/servd-plugin-console-commands
- Plugin source: https://github.com/servdhost/craft-asset-storage

Per-claim URLs appear in each reference file. Last verified against the docs on 2026-05-30. Some operational details (cron, exact plan tiers) are not in the public docs and are flagged as **Verify** where they appear.

## What's Different on Servd vs Self-Hosted

Each row is a place self-hosted habits will mislead you.

| Concern | Self-hosted | Servd |
|---|---|---|
| Config file | `.env`, `config/*.php`, web-server config | **`servd.yaml`** at repo root for the build step (optional; overrides dashboard); platform settings + runtime env vars in the Servd dashboard |
| Deploy | Whatever you've wired | **Git push-to-deploy** (GitHub/GitLab/Bitbucket or any SSH host) → Composer install + optional Node build |
| Environments | Yours to define | Fixed **local → staging → production**, **uni-directional**; `allowAdminChanges` off everywhere except local |
| Filesystem | Local disk | **Ephemeral + load-balanced** — disk writes don't persist; use Redis (Craft data cache) or a remote asset volume |
| Assets | Local or your own S3 config | **`servd/craft-asset-storage`** — S3-backed Flysystem on the `*.files.svdcdn.com` CDN, auto-separated per environment |
| Image transforms | Native / Imager-X / ImageOptimize on-server | **Off-server** transforms via the Servd Asset Platform; Imager-X uses `transformer: 'servd'` |
| Database | Whatever you installed | **MariaDB or MySQL 8**, reached over an **SSH tunnel** |
| Page caching | Blitz or similar | **Servd static caching** built in; Blitz runs **alongside** it in reverse-proxy mode (not instead of) |
| Queue | You run a worker | Default AJAX-triggered; opt into the **Dedicated Queue Runner** (paid plans) for isolated immediate processing |
| Cron | `crontab` | **Not documented** as a user-configurable feature — design around the queue (**Verify** for a given plan) |
| Redis | You install it | **Provided** — Craft's data cache is auto-mapped to a stateful Redis |
| SSH | `ssh user@server` | **Yes** — SSH sessions (used e.g. for the DB tunnel) |
| Env vars | `.env` | Dashboard-managed per environment (not a committed `.env`) |

### Servd vs Craft Cloud (quick contrast)

Both are managed Craft hosting with git deploy, ephemeral filesystems, S3 assets, off-server transforms, and dashboard env vars. Key differences for a developer:

| | Servd | Craft Cloud |
|---|---|---|
| Repo config | `servd.yaml` (build) + dashboard | `craft-cloud.yaml` |
| Asset layer | `servd/craft-asset-storage` plugin | `craftcms/cloud` bundled filesystem |
| Database | MariaDB **or** MySQL 8 | MySQL 8 / Postgres 15 (**no MariaDB**) |
| SSH | Yes | No |
| First-party CLI | None (plugin console commands + dashboard) | `craftcms/cloud` + `php craft cloud/up` |
| Caching | Servd static cache; **Blitz runs alongside** | Edge static caching; **Blitz redundant** |
| Transforms | Servd Asset Platform (`svdcdn.com`) | Cloudflare Images at the edge |
| Queue | Dedicated Queue Runner (paid) | Auto-processed |

## Common Pitfalls (Cross-Cutting)

- **Writing to disk and expecting persistence.** The filesystem is ephemeral and load-balanced — writes vanish and aren't shared across instances. Use Craft's data cache (auto-mapped to Redis) or a remote asset volume. See `references/limitations.md`.
- **Making schema/Project Config changes anywhere but local.** Servd sets `allowAdminChanges: false` on staging and production and syncs uni-directionally (local → staging → production). Make changes in local, commit, deploy. See `references/deploy-and-environments.md`.
- **Treating Blitz as a replacement for Servd's caching.** On Servd you run Blitz *alongside* the static cache in **reverse-proxy mode** (Yii Cache Storage + HTTP Generator + Servd Static Cache Purger) — Blitz's own server-rewrite mode is broken by Servd's load balancing. See `references/caching.md`.
- **Committing a `.env` for runtime config.** Runtime env vars live in the Servd dashboard per environment, not a committed `.env`. `SERVD_PROJECT_SLUG` / `SERVD_SECURITY_KEY` come from the dashboard's Assets page.
- **Using a local asset volume.** User assets must use the `servd/craft-asset-storage` filesystem so they land on the Servd Asset Platform and survive deploys. See `references/asset-storage.md`.
- **Putting `composer install` / `npm run build` in a CI action.** Servd runs both during its build step. Configure the Node build via `servd.yaml` or the dashboard instead. See `references/deploy-and-environments.md`.
- **Assuming arbitrary cron.** Servd doesn't document user-configurable cron. Move recurring work into queue jobs and the Dedicated Queue Runner. **Verify** per plan. See `references/database-and-queue.md`.
- **Choosing the wrong database habits.** Servd supports MariaDB and MySQL 8; reach the DB over the SSH tunnel, not a direct public port. See `references/database-and-queue.md`.

## Reference Files

Read the relevant reference file(s) for your task. Multiple files often apply.

**Task examples:**

- "Deploy a Craft site to Servd" → `deploy-and-environments.md`
- "Configure the Node build step / `servd.yaml`" → `deploy-and-environments.md`
- "Set up environments and sync between them" → `deploy-and-environments.md` + `local-dev.md`
- "Install Servd asset storage" → `asset-storage.md`
- "Why are my uploaded assets disappearing?" → `asset-storage.md` + `limitations.md`
- "Set up image transforms on Servd" → `asset-storage.md`
- "Enable static caching" → `caching.md`
- "Run Blitz on Servd" → `caching.md` (Blitz reverse-proxy mode)
- "Add a dynamic island to a cached page" → `caching.md` (`{% dynamicInclude %}`)
- "Connect to the Servd database" → `database-and-queue.md`
- "Set up the queue / run recurring jobs" → `database-and-queue.md`
- "Back up / restore / sync the database" → `database-and-queue.md` + `local-dev.md`
- "Set up local development for a Servd project" → `local-dev.md`
- "Pull production assets/database to local" → `local-dev.md`
- "Why does my plugin's file write fail on Servd?" → `limitations.md`
- "What plugins work on Servd?" → `limitations.md`
- "Should I use Servd or Craft Cloud?" → `limitations.md` (Servd vs Cloud) + this file's table

Load only the reference files your task needs.

| Reference | Scope | ~Lines |
|---|---|---:|
| `references/deploy-and-environments.md` | Git push-to-deploy, the build step (Composer + Node, `servd.yaml` keys, Node versions), environments (local → staging → production, uni-directional), Project Config + `allowAdminChanges`, env vars & secrets, the deploy/clone workflow | ~150 |
| `references/asset-storage.md` | `servd/craft-asset-storage` plugin (composer package, handle, install), `SERVD_PROJECT_SLUG`/`SERVD_SECURITY_KEY`, the Servd filesystem on `*.files.svdcdn.com`, per-environment dirs, off-server transforms, Imager-X (`transformer: 'servd'`) and ImageOptimize integrations | ~140 |
| `references/caching.md` | Servd static caching (enable + TTL, Full vs Tag-Based purge, exclude prefixes, `{% dynamicInclude %}` tag, CSRF injection, auto cache-busting on save, `clear-caches/servd-static-cache` + `servd-edge-caches`), and running Blitz in reverse-proxy mode | ~140 |
| `references/database-and-queue.md` | MariaDB / MySQL 8, SSH-tunnel access, automatic + manual backups (30-day retention, 90-day deleted-asset window), the Dedicated Queue Runner, the cron caveat, console sync commands | ~130 |
| `references/local-dev.md` | DDEV-based local dev (no first-party Servd local env), `SERVD_*` vars for local, `servd-asset-storage/local/pull-assets`·`push-assets`·`pull-database`·`push-database`, `servd-asset-storage/clone`, uni-directional sync discipline | ~120 |
| `references/limitations.md` | Ephemeral + load-balanced filesystem (Redis + remote volumes for runtime files), plugin/feature constraints, the documented-vs-unknown gaps (cron), the full Servd-vs-Craft-Cloud comparison, and the repo **detection signals** (`servd/craft-asset-storage`, `servd.yaml`, `SERVD_*` env vars) | ~140 |
