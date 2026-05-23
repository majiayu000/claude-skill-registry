---
name: wp-env-cli
description: Use when running WordPress CLI commands, managing wp-env environments, debugging WordPress sites, or working with databases in local development. Triggers include wp-cli, wp-env, database queries, plugin activation, user management, cache clearing, or WordPress debugging.
---

# wp-env CLI Management

## Overview

wp-env wraps Docker to provide WordPress development environments. All wp-cli commands run through `wp-env run cli wp <command>`. This skill covers common operations and troubleshooting.

## Quick Reference

| Task | Command |
|------|---------|
| Run wp-cli command | `wp-env run cli wp <command>` |
| Run in test env | `wp-env run tests-cli wp <command>` |
| Open shell | `wp-env run cli bash` |
| View logs | `wp-env logs` |
| Reset database | `wp-env clean all && wp-env start` |
| Start with debug | `wp-env start --xdebug=debug` |

## Running WP-CLI Commands

**Basic syntax:**
```bash
wp-env run cli wp <command>
```

**Common operations:**
```bash
# User management
wp-env run cli wp user list
wp-env run cli wp user create dev dev@example.com --role=administrator

# Plugin management
wp-env run cli wp plugin list
wp-env run cli wp plugin activate woocommerce
wp-env run cli wp plugin deactivate --all

# Database operations
wp-env run cli wp db query "SELECT * FROM wp_options WHERE option_name='siteurl'"
wp-env run cli wp db export /var/www/html/backup.sql
wp-env run cli wp db import /var/www/html/backup.sql

# Option management
wp-env run cli wp option get siteurl
wp-env run cli wp option update blogname "Dev Site"

# Cache and transients
wp-env run cli wp cache flush
wp-env run cli wp transient delete --all

# WooCommerce specific
wp-env run cli wp wc product list --user=1
wp-env run cli wp wc order list --user=1
```

## Working Directory Context

For commands in plugin directories, use `--env-cwd`:
```bash
wp-env run cli --env-cwd=wp-content/plugins/woocommerce composer install
wp-env run cli --env-cwd=wp-content/plugins/my-plugin npm run build
```

## Environment Management

```bash
# Start/stop
wp-env start              # Start environment
wp-env start --update     # Update and restart
wp-env stop               # Stop containers

# Reset options
wp-env clean development  # Reset dev database only
wp-env clean tests        # Reset test database only
wp-env clean all          # Reset both databases
wp-env destroy            # Remove everything (nuclear)

# Debugging
wp-env start --xdebug=debug           # Enable Xdebug
wp-env start --xdebug=profile,trace   # Profiling
wp-env logs                           # View PHP/Docker logs
wp-env logs tests                     # Test environment logs
```

## Database Access

- **Host:** 127.0.0.1 (not localhost)
- **Port:** Check with `docker ps` for mysql container port
- **User:** root
- **Password:** password

Direct MySQL access:
```bash
wp-env run cli mysql -u root -ppassword wordpress
```

## Common Gotchas

1. **Always use `wp-env run cli`** - Running `wp` directly won't work
2. **Paths are container paths** - `/var/www/html/` is the WordPress root inside container
3. **Symlinked plugins** - Changes in ~/Repos reflect immediately (no copy needed)
4. **Database names** - Development: `wordpress`, Tests: `tests-wordpress`
5. **Shell escaping** - Complex queries may need extra escaping: `wp-env run cli wp db query "SELECT * FROM wp_options"`
