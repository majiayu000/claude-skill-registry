---
name: ddev
description: "DDEV local development environment for Craft CMS projects. ALWAYS load this skill when running any ddev command, configuring .ddev/config.yaml, or troubleshooting local container issues. Covers: config.yaml settings (project type, PHP/Node versions, database, docroot), shorthand commands (ddev composer, ddev craft, ddev npm), add-ons (ddev add-on get for Redis, Mailpit), custom commands (.ddev/commands/), Vite dev server exposure (web_extra_exposed_ports, web_extra_daemons), database import/export (ddev import-db, ddev export-db, ddev craft db/backup), Xdebug toggling (ddev xdebug on/off), sharing local sites (ddev share, temporary public URLs), and troubleshooting (ddev poweroff, ddev logs, ddev describe, ddev delete, port conflicts, container restart issues). Triggers on: ddev start/stop/restart, ddev craft, ddev composer, ddev npm, ddev ssh, ddev import-db, ddev export-db, ddev xdebug, ddev share, ddev add-on, ddev poweroff, ddev describe, ddev logs, .ddev/config.yaml, web_extra_exposed_ports, web_extra_daemons, PHP version or Node version in local dev, database backup/restore locally, ran npm/composer on host instead of ddev, wrong node_modules architecture, local dev environment for Craft CMS. NOT for production deployment, CI/CD pipelines, GitHub Actions, or server configuration. NOT for Docker/container usage outside of DDEV."
---

# DDEV for Craft CMS Development

## Companion Skills — Always Load Together

When this skill triggers, also load:

- **`craftcms`** — Plugin/module development. Required when DDEV commands involve Craft CLI (`ddev craft make`, `ddev craft migrate`, `ddev craft project-config`).
- **`craft-php-guidelines`** — PHP coding standards. Required when DDEV commands involve code quality tooling (`ddev composer check-cs`, `ddev composer phpstan`, `ddev craft pest/test`).

## Documentation

- DDEV docs: https://docs.ddev.com/en/stable/
- Craft CMS quickstart: https://docs.ddev.com/en/stable/users/quickstart/#craft-cms
- Configuration reference: https://docs.ddev.com/en/stable/users/configuration/config/
- Custom commands: https://docs.ddev.com/en/stable/users/extend/custom-commands/
- Additional services: https://docs.ddev.com/en/stable/users/extend/additional-services/
- Vite integration: https://docs.ddev.com/en/stable/users/usage/developer-tools/#nodejs

When unsure about a DDEV feature, `WebFetch` the relevant docs page.

## Common Pitfalls

- Using `ddev exec composer install` instead of `ddev composer install` — DDEV shorthand commands handle path resolution and environment setup. Always use the shorthand.
- Forgetting `ddev craft up` does both `migrate/all` and `project-config/apply` — no need to run them separately after pulls or deploys.
- Exposing the Vite dev server with `ports` instead of `web_extra_exposed_ports` — `ports` causes conflicts when running multiple DDEV projects. `web_extra_exposed_ports` routes through Traefik and works with HTTPS.
- Running `ddev composer global require` — global packages install inside the container and vanish on restart. Install project-level dependencies only.
- Setting `nodejs_version` but running `npm install` on the host — Node must run inside the container via `ddev npm` to match the configured version.
- Editing `.ddev/config.yaml` while containers are running without restarting — changes to config require `ddev restart` to take effect.
- Using `ddev import-db` without `--target-db=db` on multi-database setups — the default target is `db`, but if you've configured additional databases, be explicit.
- Adding `#ddev-generated` to custom commands you've customized — DDEV overwrites files with this comment during updates. Only use it for add-on-managed commands. Custom commands you maintain should omit it.

## Shorthand Commands

Always use DDEV shorthand over `ddev exec`:

```bash
ddev composer install          # not ddev exec composer install
ddev craft up                  # not ddev exec php craft up
ddev npm install               # not ddev exec npm install
ddev craft make service        # scaffolding
```

## Craft CMS Project Type

```yaml
# .ddev/config.yaml
name: my-craft-site
type: craftcms
docroot: web
php_version: "8.3"
database:
  type: mysql
  version: "8.0"
nodejs_version: "20"
```

DDEV auto-injects: `CRAFT_DB_SERVER`, `CRAFT_DB_USER`, `CRAFT_DB_PASSWORD`, `CRAFT_DB_DATABASE`, `PRIMARY_SITE_URL`.

## Common Commands

```bash
ddev start                     # Start the project
ddev stop                      # Stop the project
ddev restart                   # Restart containers
ddev ssh                       # SSH into web container
ddev describe                  # Show project info and URLs
ddev logs                      # View container logs
ddev import-db --file=dump.sql # Import database
ddev export-db --file=dump.sql # Export database
ddev xdebug on                 # Enable Xdebug
ddev craft db/backup           # Craft database backup
```

## Post-Install Auto-Run

Composer scripts auto-run `craft up` after install/update:

```json
{
    "scripts": {
        "post-craft-update": [
            "@php craft install/check && php craft up --interactive=0 || exit 0"
        ],
        "post-update-cmd": "@post-craft-update",
        "post-install-cmd": "@post-craft-update"
    }
}
```

No need to manually run `ddev craft migrate/all` or `ddev craft project-config/apply` — `ddev craft up` does both, and it auto-runs after `ddev composer install/update`.

## Add-ons

```bash
ddev add-on get ddev/ddev-redis       # Install Redis
ddev add-on get ddev/ddev-mailpit     # Install Mailpit
ddev add-on list                       # List installed add-ons
ddev add-on remove ddev/ddev-redis    # Remove add-on
```

## Custom Commands

Place scripts in `.ddev/commands/web/` (container) or `.ddev/commands/host/` (host):

```bash
#!/usr/bin/env bash
## Description: Run ECS code style check
## Usage: check-cs
## Example: ddev check-cs

cd /var/www/html && composer check-cs
```

Note: omit `#ddev-generated` on custom commands you maintain — DDEV overwrites files with that comment during updates. Only add-on-managed commands should include it.

## Troubleshooting

```bash
ddev poweroff                  # Stop all DDEV projects
ddev debug router              # Debug router configuration
ddev debug capabilities        # Check Docker capabilities
ddev delete --omit-snapshot    # Remove project without snapshot
```
