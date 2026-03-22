---
name: frappe-ops-bench
description: >
  Use when running bench commands, managing sites, configuring multi-tenancy, or setting up domains.
  Prevents misconfigured bench environments, broken site routing, and DNS mismatches.
  Covers bench CLI commands, site creation, bench init, multi-tenancy setup, DNS-based routing, common-site-config.
  Keywords: bench, site, multi-tenancy, domains, bench init, bench new-site, bench setup, common_site_config.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Bench CLI Complete Reference

Complete bench CLI reference for site management, app lifecycle, configuration, and multi-tenancy.

**Version**: v14/v15/v16

---

## Quick Reference — Essential Commands

| Task | Command |
|------|---------|
| Create bench | `bench init myproject --frappe-branch version-15` |
| Create site | `bench new-site mysite.localhost --admin-password admin` |
| Set default site | `bench use mysite.localhost` |
| Get app | `bench get-app erpnext --branch version-15` |
| Install app | `bench --site mysite install-app erpnext` |
| Start dev server | `bench start` |
| Run migrations | `bench --site mysite migrate` |
| Build assets | `bench build --app myapp` |
| Backup site | `bench --site mysite backup` |
| Restore backup | `bench --site mysite restore /path/to/backup.sql.gz` |
| Open console | `bench --site mysite console` |
| Open DB shell | `bench --site mysite mariadb` |
| Check scheduler | `bench doctor` |
| View pending jobs | `bench show-pending-jobs` |
| Update everything | `bench update` |
| Drop site | `bench drop-site mysite --force` |

---

## Workflow 1: Creating a New Bench

```bash
# Initialize bench with specific Frappe version
bench init myproject --frappe-branch version-15

# With Python version
bench init myproject --frappe-branch version-15 --python python3.11

# Enter bench directory (REQUIRED for all subsequent commands)
cd myproject
```

**What `bench init` creates:**

```
myproject/
├── apps/           # Installed Frappe apps (frappe is default)
├── sites/          # All sites and shared config
│   └── common_site_config.json
├── config/         # Redis, Procfile, supervisor configs
├── env/            # Python virtual environment
├── logs/           # Log files
└── Procfile        # Process definitions for bench start
```

### Critical Rules

- **ALWAYS** specify `--frappe-branch` to pin Frappe version
- **ALWAYS** run commands from inside the bench directory
- **NEVER** run bench commands as root — use a dedicated frappe user

---

## Workflow 2: Site Management

### Creating Sites

```bash
# Basic site creation
bench new-site mysite.localhost --admin-password admin

# With specific database
bench new-site mysite.localhost --db-name mysite_db --admin-password admin

# With MariaDB root password
bench new-site mysite.localhost --mariadb-root-password rootpass --admin-password admin

# Install apps during creation
bench new-site mysite.localhost --admin-password admin --install-app erpnext
```

### Setting Default Site

```bash
bench use mysite.localhost
# OR set environment variable for current session:
export FRAPPE_SITE=mysite.localhost
```

### Dropping a Site

```bash
bench drop-site mysite.localhost --force
# Deletes database and archives site directory
```

### Site Directory Structure

```
sites/mysite.localhost/
├── site_config.json     # Site-specific config (db credentials)
├── private/             # Auth-required files, backups
├── public/              # Publicly accessible files
├── locks/               # Scheduler lock files
└── task-logs/           # Scheduler task logs
```

---

## Workflow 3: App Management

```bash
# Download app from GitHub
bench get-app erpnext --branch version-15
bench get-app https://github.com/org/custom-app.git --branch main

# Install app on a site
bench --site mysite install-app erpnext

# List installed apps
bench --site mysite list-apps

# Remove app from site (creates backup first)
bench --site mysite uninstall-app custom_app

# Remove app from bench entirely
bench remove-app custom_app

# Switch app branch
bench switch-to-branch version-15 erpnext frappe

# Exclude app from updates
bench exclude-app custom_app

# Re-include app in updates
bench include-app custom_app
```

### Critical Rules

- **ALWAYS** `get-app` before `install-app` — get downloads, install activates
- **ALWAYS** backup before `uninstall-app` — it deletes app-related data
- **NEVER** manually delete app folders — use `bench remove-app`

---

## Workflow 4: bench update — What It Does

```bash
# Full update (pull + migrate + build + restart)
bench update

# Update specific app only
bench update --pull --app erpnext

# Skip build step
bench update --no-build

# Skip backup
bench update --no-backup

# Reset to upstream (DESTROYS local changes)
bench update --reset
```

**`bench update` executes these steps in order:**
1. Backup all sites
2. Pull latest code for all apps (`git pull`)
3. Install Python/Node requirements
4. Build static assets (`bench build`)
5. Run migrations on all sites (`bench migrate`)
6. Restart bench processes

### Critical Rules

- **ALWAYS** run `bench update` in a screen/tmux session — it takes time
- **NEVER** use `--reset` in production without understanding it does `git reset --hard`
- **ALWAYS** test updates on staging first

---

## Workflow 5: bench migrate

```bash
# Migrate specific site
bench --site mysite migrate

# Migrate all sites
bench --site all migrate

# Check if safe to migrate (no pending jobs)
bench --site mysite ready-for-migration
```

**What `bench migrate` does:**
1. Runs schema sync (DocType changes → database)
2. Runs patches (data migrations)
3. Rebuilds search index
4. Syncs translations
5. Rebuilds Dashboard cache

### When to Migrate

- After `bench update` (done automatically)
- After changing hooks.py
- After adding/modifying DocTypes
- After pulling code changes
- **NEVER** skip migrate after code changes — leads to schema mismatches

---

## Workflow 6: bench build

```bash
# Build all apps
bench build

# Build specific app
bench build --app myapp

# Build with bundle analyzer
bench build --app myapp --production

# Watch mode (auto-rebuild on file changes)
bench watch
```

### When to Build

- After changing JS/CSS files
- After `bench get-app` (done automatically)
- After modifying `package.json`
- **ALWAYS** build after modifying client-side assets

---

## Workflow 7: Console and Database Access

```bash
# IPython console (with Frappe loaded)
bench --site mysite console
# In console:
# >>> frappe.get_doc("Sales Invoice", "INV-001")
# >>> frappe.db.sql("SELECT name FROM `tabUser` LIMIT 5")

# Auto-reload on code changes
bench --site mysite console --autoreload

# MariaDB shell
bench --site mysite mariadb
# >>> SELECT name, email FROM tabUser LIMIT 5;

# PostgreSQL shell
bench --site mysite postgres

# Execute a method directly
bench --site mysite execute myapp.tasks.daily_cleanup
bench --site mysite execute myapp.api.process --kwargs '{"name": "INV-001"}'

# Make authenticated request as Administrator
bench --site mysite request GET /api/resource/User
```

---

## Workflow 8: Backup and Restore

```bash
# Backup (database + files)
bench --site mysite backup
# Creates: sites/mysite/private/backups/
#   YYYY-MM-DD_HHMMSS-mysite-database.sql.gz
#   YYYY-MM-DD_HHMMSS-mysite-files.tar
#   YYYY-MM-DD_HHMMSS-mysite-private-files.tar

# Backup all sites
bench backup-all-sites

# Backup with encryption
bench --site mysite backup --backup-encryption-key mykey

# Restore from backup
bench --site mysite restore /path/to/database.sql.gz

# Restore with files
bench --site mysite restore /path/to/database.sql.gz \
  --with-public-files /path/to/files.tar \
  --with-private-files /path/to/private-files.tar

# Partial restore
bench --site mysite partial-restore /path/to/database.sql.gz
```

### Critical Rules

- **ALWAYS** backup before `bench update`, `uninstall-app`, or `drop-site`
- Backups older than 24 hours auto-deleted by default — configure `keep_backups_for_hours`
- **ALWAYS** test restore on a staging site before relying on a backup

---

## Workflow 9: Scheduler and Background Jobs

```bash
# Enable/disable scheduler
bench --site mysite scheduler enable
bench --site mysite scheduler disable
bench --site mysite scheduler pause
bench --site mysite scheduler resume

# Check scheduler health
bench doctor

# View queued jobs
bench show-pending-jobs

# Purge pending jobs
bench --site mysite purge-jobs

# Manually trigger scheduler event
bench --site mysite trigger-scheduler-event hourly

# Start worker manually (for debugging)
bench worker --queue short
```

---

## Workflow 10: Multi-Tenancy

### DNS-Based Routing (Recommended)

```bash
# Enable DNS multi-tenancy
bench config dns_multitenant on

# Create sites with proper hostnames
bench new-site site1.example.com --admin-password admin
bench new-site site2.example.com --admin-password admin

# Regenerate nginx config
bench setup nginx

# Reload nginx
sudo service nginx reload
```

Requests are routed by matching the `Host` header to site names.

### Port-Based Routing (Alternative)

```bash
bench config dns_multitenant off
bench new-site site2.localhost --admin-password admin
bench set-nginx-port site2.localhost 8082
bench setup nginx
sudo service nginx reload
```

### Custom Domain Mapping

```bash
# Add domain to site
bench setup add-domain site1.example.com --site mysite
bench setup nginx
sudo service nginx reload
```

---

## Configuration: common_site_config.json

Located at `sites/common_site_config.json` — applies to ALL sites.

### Essential Keys

| Key | Default | Purpose |
|-----|---------|---------|
| `background_workers` | 1 | Number of background job workers |
| `developer_mode` | false | Auto-sync DocType changes to files |
| `dns_multitenant` | false | Enable DNS-based multi-tenancy |
| `gunicorn_workers` | 2 | Web server worker count (min: 2) |
| `maintenance_mode` | 0 | Take all sites offline |
| `pause_scheduler` | 0 | Pause job scheduler |
| `serve_default_site` | — | Default site when host not matched |
| `server_script_enabled` | false | Enable Server Scripts |
| `scheduler_tick_interval` | 60 | Seconds between scheduler checks |
| `webserver_port` | 8000 | Development server port |
| `socketio_port` | 9000 | Socket.IO port |
| `live_reload` | false | Auto-reload on asset rebuild |

### Redis Configuration

| Key | Default |
|-----|---------|
| `redis_cache` | `redis://localhost:13000` |
| `redis_queue` | `redis://localhost:11000` |
| `redis_socketio` | `redis://localhost:13000` |

### Setting Config Values

```bash
# Set common config (all sites)
bench config set-common-config -c background_workers 4
bench config set-common-config -c developer_mode 1

# Set site-specific config
bench --site mysite set-config developer_mode 1
bench --site mysite set-config maintenance_mode 1

# View current config
bench --site mysite show-config
```

---

## Configuration: site_config.json

Per-site config at `sites/<sitename>/site_config.json`.

### Mandatory Keys

| Key | Purpose |
|-----|---------|
| `db_type` | `mariadb` or `postgres` |
| `db_name` | Database name |
| `db_password` | Database password |

### Important Optional Keys

| Key | Purpose |
|-----|---------|
| `admin_password` | Administrator initial password |
| `host_name` | Full site URL (with protocol) |
| `install_apps` | Apps to install on restore/reinstall |
| `allow_cors` | CORS origins (`"*"`, URL, or array) |
| `max_file_size` | Upload limit (default: 10MB) |
| `mute_emails` | Disable all outgoing email |
| `logging` | Debug level (0-2, level 2 shows SQL queries) |

### Environment Variable Overrides

Environment variables override config files. Key mappings: `FRAPPE_REDIS_QUEUE`, `FRAPPE_REDIS_CACHE`, `FRAPPE_DB_HOST`, `FRAPPE_DB_PORT`, `FRAPPE_DB_NAME`, `FRAPPE_DB_PASSWORD`.

**Priority**: Environment Variable > site_config.json > common_site_config.json > Default

---

## Production Setup

```bash
sudo bench setup production frappe-user   # nginx + supervisor + fail2ban
bench setup lets-encrypt mysite.example.com  # SSL
sudo bench restart                          # Restart services
bench disable-production                    # Back to development
```

---

## Version Differences

| Feature | V14 | V15 | V16 |
|---------|:---:|:---:|:---:|
| bench init | Yes | Yes | Yes |
| Scheduler tick interval | ~240s | ~240s | **60s** |
| `db_user` config (separate) | No | No | **Yes** |
| `console --autoreload` | No | Yes | Yes |
| `trim-tables` command | No | Yes | Yes |
| `trim-database` command | No | Yes | Yes |
| `request` command | No | Yes | Yes |
| Gettext translations | No | No | **Yes** |

---

## Reference Files

| File | Contents |
|------|----------|
| [commands.md](references/commands.md) | Full command reference with all options |
| [examples.md](references/examples.md) | Common workflow examples |
| [custom-commands.md](references/custom-commands.md) | Creating custom bench CLI commands with Click |
| [anti-patterns.md](references/anti-patterns.md) | Common bench mistakes and fixes |
