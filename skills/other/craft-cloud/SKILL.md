---
name: craft-cloud
description: "Craft Cloud — Pixel & Tonic's serverless hosting platform for Craft CMS. Covers craft-cloud.yaml configuration, the Build → Migrate → Release deploy pipeline, the craftcms/cloud extension package, edge image transforms via Cloudflare, edge static caching with cache.rules + ESI, Cloud-managed S3 filesystem, MySQL 8 / Postgres 15 databases (no MariaDB, no tablePrefix), Console-based command runner and scheduled cron (once-per-hour minimum), auto-handled queue jobs, custom domains and SSL, preview environments per branch, Cloud limitations (ephemeral filesystem, no SSH, no .htaccess, no built-in mail), plugin development requirements for Cloud compatibility, and self-hosted → Cloud migration. Triggers on: craft-cloud.yaml, craftcms/cloud package, cloud.esi(), php craft cloud/up, php craft cloud/setup, App::isEphemeral(), CRAFT_EPHEMERAL, edge.craft.cloud, preview.craft.cloud, CRAFT_CLOUD_PROJECT_ID, CRAFT_CLOUD_ENVIRONMENT_ID, CRAFT_CLOUD_CDN_BASE_URL, Build → Migrate → Release, Cloud filesystem, Cloud-compatible plugin, Cloudflare Images at edge, AssetsFs, static-caching rules, ESI islands, deploy to Craft Cloud, migrate to Craft Cloud, self-hosted to Cloud, Craft Cloud quotas, Craft Cloud regions. Do NOT trigger for generic Craft deployment (Forge, Servd, bare metal) — that lives in craftcms/deployment.md. Do NOT trigger for general DDEV local dev unrelated to Cloud parity."
---

# Craft Cloud — Serverless Hosting for Craft CMS

Reference for Craft Cloud, Pixel & Tonic's serverless hosting platform for Craft CMS. Covers the `craft-cloud.yaml` config file, the Build → Migrate → Release deploy pipeline, the `craftcms/cloud` extension, edge image transforms and static caching, the Cloud filesystem, plugin Cloud-compatibility requirements, and self-hosted → Cloud migration.

This skill is scoped to **Craft Cloud specifically** — what's different on Cloud vs running Craft yourself on Forge, Servd, or bare metal. For generic Craft deployment (build artifacts, project config sync, atomic deploys on traditional hosts), see the `craftcms` skill's `deployment.md`.

## Companion Skills — Load When Needed

- **`craftcms`** — When the Cloud topic intersects plugin or module PHP work (e.g. `App::isEphemeral()` guards in services, asset-bundle constraints, queue job design for the 15-minute cap).
- **`craft-site`** — When Cloud intersects front-end templating (ESI islands inside cached pages, edge image transform usage, `{% expires %}` opt-outs for static caching).
- **`ddev`** — For the local-dev parity recipe (matching PHP/DB versions, simulating the ephemeral filesystem locally).
- **`craft-php-guidelines`** — When editing plugin PHP to add Cloud-compatibility checks.

## Documentation

Authoritative sources used to write this skill:

- Craft Cloud docs landing: https://craftcms.com/docs/cloud/
- Configuration reference: https://craftcms.com/docs/cloud/config
- Deployment pipeline: https://craftcms.com/docs/cloud/deployment
- Builds: https://craftcms.com/docs/cloud/builds
- Compatibility & limitations: https://craftcms.com/docs/cloud/compatibility
- Assets & transforms: https://craftcms.com/docs/cloud/assets
- Static caching: https://craftcms.com/docs/cloud/static-caching
- Plugin development: https://craftcms.com/docs/cloud/plugin-development
- Cloud extension source: https://github.com/craftcms/cloud-extension-yii2

Per-claim URLs appear in each reference file. Last verified against the docs and `craftcms/cloud-extension-yii2@main` on 2026-05-28.

## What's Different on Cloud vs Self-Hosted

A quick orientation table. Each row is a place self-hosted habits will mislead you.

| Concern | Self-hosted | Cloud |
|---|---|---|
| Config file | `.env`, `config/general.php`, `config/db.php`, your web-server config | **`craft-cloud.yaml`** at repo root for platform settings; runtime env vars set in Craft Console UI (not `.env`) |
| Deploy | Whatever you've wired (Forge, GitHub Actions, rsync) | Git push → automatic **Build → Migrate → Release** (15-min build cap) |
| Filesystem | Local disk or your own S3/R2 config | **Ephemeral** Lambda filesystem; use `App::isEphemeral()` to gate writes; user assets must use the Cloud-bundled S3-backed filesystem type |
| Database | Whatever you've installed | **MySQL 8.0 or Postgres 15 only** — no MariaDB, no `tablePrefix`, no `db.php` touching, no `CRAFT_DB_*` overrides |
| Queue jobs | You run a worker (systemd, supervisor, cron) | **Auto-processed** by Cloud — don't schedule the runner; cap each job at 15 minutes |
| Cron | `crontab -e`, any frequency | Craft Console UI only; **once per hour minimum** |
| Image transforms | ImageOptimize / Imager-X / native | **Edge transforms** via Cloudflare Images — no template changes needed, but ImageOptimize is incompatible |
| Page caching | Blitz or similar | **Edge static caching** via `cache.rules` in `craft-cloud.yaml`; tag-based auto-invalidation |
| Dynamic islands in cached pages | Per-cache-driver workaround | First-class **`cloud.esi(...)`** Twig helper |
| Logs | Files in `storage/logs/` | `Craft::info/warning/error()` only — no file-tailing UI; Console command output is the de-facto surface |
| Mail | sendmail or any adapter | **No built-in mail** — bring your own SMTP/Postmark/SES/Resend |
| SSH | `ssh user@server` | None — Console command runner only (255-char cap, 15-min cap) |
| Server rewrites | `.htaccess` / nginx config | `redirects:` and `rewrites:` keys in `craft-cloud.yaml` |
| Custom domains | DNS provider + cert | DNS + ownership TXT + CNAME to `edge.craft.cloud`; auto SSL via Cloudflare |
| Preview environments | Your CI | Per-branch only — **no per-PR previews documented** |

## Common Pitfalls (Cross-Cutting)

- **Writing to disk without an `App::isEphemeral()` guard.** Lambda's filesystem is ephemeral and writes are lost between requests. Plugins, services, and migrations all need to check and use the Path service (`Craft::$app->getPath()->getTempPath()`/`getStoragePath()`/`getCachePath()`) for transient writes. See `references/extension.md` (App::isEphemeral) and `references/plugin-development.md`.
- **Configuring `db.php` or setting `CRAFT_DB_*` env vars.** Cloud auto-wires the database connection through the extension; manual config can break it. See `references/database.md`.
- **Using `tablePrefix`.** Unsupported on Cloud. Run `php craft db/drop-table-prefix` before migrating. See `references/migration.md`.
- **Choosing MariaDB.** Cloud only supports MySQL 8.0 and Postgres 15.
- **Scheduling your own queue runner.** Cloud auto-processes queue jobs — adding a scheduled command for the queue runner is redundant and may conflict.
- **Trying to schedule cron more often than hourly.** Cloud's UI enforces a one-hour minimum. Design recurring tasks around this floor or move the work into queue jobs triggered by other events.
- **`{{ csrfInput() }}` in cacheable templates.** Forces a cookie, busts edge static caching. Use the `csrfInput()` function instead, which renders an async input compatible with `asyncCsrfInputs` (force-enabled on Cloud).
- **`.htaccess` rules or nginx config in the repo.** Won't be honored — move to `redirects:` / `rewrites:` in `craft-cloud.yaml`. See `references/config-file.md`.
- **Writing to log files.** No persistent filesystem. Use `Craft::info/warning/error()` and the logger routes to Cloud's log target automatically. See `references/extension.md`.
- **Assuming SSH access.** There is none. The Console command runner is the only way to execute commands, with a 255-character argument cap and 15-minute timeout.
- **Forked Git repos.** Cloud can't deploy from forks — must be the upstream repository.
- **Expecting per-PR preview environments.** Cloud supports per-branch environments only; no automatic ephemeral environment per pull request.
- **Default `sendmail` adapter.** Will not deliver mail. Configure SMTP/Postmark/SES/Resend explicitly. See `references/limitations.md` (Mail).
- **Using ImageOptimize on Cloud.** Cloud handles transforms at the edge via Cloudflare Images — ImageOptimize duplicates the work and can conflict. See `references/assets-and-transforms.md`.

## Reference Files

Read the relevant reference file(s) for your task. Multiple files often apply.

**Task examples:**

- "Set up a new Craft project on Cloud" → `config-file.md` + `deploy-pipeline.md` + `extension.md`
- "Configure `craft-cloud.yaml` for PHP and Node versions" → `config-file.md`
- "Add redirects in `craft-cloud.yaml`" → `config-file.md` (Redirects and Rewrites)
- "What happens during deploy?" → `deploy-pipeline.md`
- "Set build-time env vars" → `deploy-pipeline.md` (Build-time vs runtime variables)
- "What does `php craft cloud/up` do?" → `extension.md` (cloud/up internals)
- "Add an ESI island inside a cached page" → `caching-and-edge.md`
- "Edge static caching rules" → `caching-and-edge.md`
- "Migrate user assets from self-hosted to Cloud" → `assets-and-transforms.md` + `migration.md`
- "Make this plugin Cloud-compatible" → `plugin-development.md`
- "Why does my plugin's file write silently fail on Cloud?" → `plugin-development.md` (Ephemeral filesystem) + `extension.md` (App::isEphemeral)
- "Set up a custom domain" → `domains.md`
- "Schedule a recurring command" → `commands-and-cron.md` (hourly minimum)
- "Run a one-off command on Cloud" → `commands-and-cron.md` (Console command runner)
- "Configure SMTP on Cloud" → `limitations.md` (Mail) + `craftcms/email.md`
- "Set up local DDEV to match Cloud" → `local-dev.md`
- "Move a self-hosted Craft site to Cloud" → `migration.md`
- "What plugins work on Cloud?" → `limitations.md` (Plugin compatibility — community knowledge)

Load only the reference files your task needs.

| Reference | Scope | ~Lines |
|---|---|---:|
| `references/config-file.md` | Full `craft-cloud.yaml` key reference: `php-version`, `node-version`, `node-path`, `npm-script`, `artifact-path`, `app-path`, `webroot`, `cache.rules`, `redirects`, `rewrites` | 154 |
| `references/deploy-pipeline.md` | Build → Migrate → Release flow, On Push vs Manual triggers, 15-min build cap, build-time system vars (`CRAFT_CLOUD_*`, `GIT_SHA`), runtime env vars in Console, failed-migration rollback semantics | 130 |
| `references/extension.md` | `craftcms/cloud` package: Yii2 module bootstrap, `App::isEphemeral()`, Path service usage, `cloud.esi()` Twig helper, `cloud/up` internals (verified from source), asset-bundle CDN publisher, binary response auto-upload, log target | 201 |
| `references/assets-and-transforms.md` | Cloud filesystem type (mandatory `assets/` subpath), `aws s3 sync` migration, edge image transforms (70MB / 100MP / 12,000px limits, AVIF 1,600px cap, stretch-mode constraint), no template-side changes required | 87 |
| `references/database.md` | MySQL 8.0 / Postgres 15 only (no MariaDB), `tablePrefix` ban, `php craft db/drop-table-prefix`, auto-wired connection, nightly + on-demand backups, restore commands | 105 |
| `references/caching-and-edge.md` | Static caching rules (`pattern` + `query-string.mode`/`keys` + `session`, first-match wins), opt-outs (`{% expires %}`, `setNoCacheHeaders()`), `asyncCsrfInputs` force-enabled, `cloud.esi(...)` for dynamic islands (scalar vars only, no nesting), tag-based auto-invalidation | 223 |
| `references/domains.md` | DNS setup (`_cf-custom-hostname` TXT, CNAME to `edge.craft.cloud`, apex A records, Orange-to-Orange Cloudflare), preview URL format, auto SSL, `www` not auto-added, extra-domain pricing | 104 |
| `references/commands-and-cron.md` | Console command runner (no SSH, 255-char cap, 15-min cap, no shell interpolation), scheduled commands (hourly minimum, max 5 per env), queue jobs auto-processed (don't schedule a runner), 15-min per-job cap, batched jobs for long work | 143 |
| `references/plugin-development.md` | Cloud-compatible plugin checklist: asset-bundle constraints, `App::isEphemeral()` gating, Path service, `Craft::info()` for logs, queue-job budgeting, cookie-free design, `csrfInput()` function (CSRF-token leakage warning), `sendContentAsFile()` auto-handling, asset-select preference, Craft 4.6+ minimum | 234 |
| `references/migration.md` | Self-hosted → Cloud cutover: audit (table prefix, MariaDB, file writes, `.htaccess`, third-party S3 plugins), `php craft db/drop-table-prefix`, asset migration via `aws s3 sync`, DNS cutover sequence, project-config sync | 132 |
| `references/local-dev.md` | DDEV recipe to mirror Cloud: matching PHP from `craft-cloud.yaml`, DB engine + version, the Cloud extension self-detection and no-op locally, optional `CRAFT_EPHEMERAL` for testing guards, S3 emulation pointers | 145 |
| `references/limitations.md` | Documented unsupported features (MariaDB, tablePrefix, .htaccess, SSH, sendmail, devMode in prod, 6MB response cap, 60s request timeout, 200MB upload cap, no env cloning, no region change, no per-PR previews, CP DB-backup utility disabled, forked repos can't deploy) + community-knowledge plugin compatibility matrix (ImageOptimize, Imager-X, Blitz, Typesense, etc.) clearly marked as not Pixel & Tonic-blessed + mail strategy + logging gap | 196 |
