---
name: wp-wpcli-and-ops
description: "Use when working with WP-CLI for WordPress operations: safe search-replace, db export/import, plugin/theme management, cron, cache flushing, multisite, and automation with wp-cli.yml."
compatibility: "Targets WordPress 6.9+ (PHP 8.0+). Requires WP-CLI in the execution environment."
---

# WP-CLI and Ops

## When to use

Use this skill for WordPress operational work:

- `wp search-replace` (URL changes, domain migrations)
- DB export/import, resets, inspections (`wp db *`)
- Plugin/theme install/activate/update
- Cron event listing/running
- Cache/rewrite flushing
- Multisite operations (`wp site *`, `--url`, `--network`)
- Building repeatable scripts (`wp-cli.yml`, shell scripts)

## Inputs required

- Environment (dev/staging/prod) and safety constraints
- Site root path: `--path=<wordpress-root>`
- Multisite: `--url=<site-url>` if applicable
- Any restrictions (no writes, no plugin installs, maintenance window)

## Procedure

### 0) Safety guardrails

WP-CLI commands can be destructive. Before any write operation:

1. Confirm environment (dev/staging/prod)
2. Confirm targeting (path/url)
3. Make a backup for risky operations

### 1) Safe URL/domain migration

**Step-by-step:**

```bash
# 1. Backup database first
wp db export backup-$(date +%Y%m%d).sql --path=/path/to/wp

# 2. Dry run to review impact
wp search-replace 'old-domain.com' 'new-domain.com' --dry-run --path=/path/to/wp

# 3. Execute the replacement
wp search-replace 'old-domain.com' 'new-domain.com' --path=/path/to/wp

# 4. Flush caches and rewrites
wp cache flush --path=/path/to/wp
wp rewrite flush --path=/path/to/wp
```

**Common flags:**

| Flag | Purpose |
|------|---------|
| `--dry-run` | Preview changes without applying |
| `--precise` | Exact match only |
| `--recurse-objects` | Handle serialized data in objects |
| `--all-tables` | Include non-WP tables |
| `--skip-columns=guid` | Skip GUID column (recommended) |

### 2) Database operations

```bash
# Export
wp db export backup.sql

# Import
wp db import backup.sql

# Query
wp db query "SELECT ID, post_title FROM wp_posts LIMIT 5"

# Optimize
wp db optimize

# Reset (DESTRUCTIVE)
wp db reset --yes
```

### 3) Plugin/theme management

```bash
# List plugins
wp plugin list

# Install and activate
wp plugin install query-monitor --activate

# Deactivate
wp plugin deactivate plugin-name

# Update all
wp plugin update --all

# Same for themes
wp theme list
wp theme install theme-name --activate
```

### 4) Cron management

```bash
# List scheduled events
wp cron event list

# Run a specific event
wp cron event run my_event_hook

# Test cron is working
wp cron test
```

### 5) Cache operations

```bash
# Flush object cache
wp cache flush

# Flush transients
wp transient delete --all

# Flush rewrite rules
wp rewrite flush
```

### 6) Multisite operations

```bash
# List all sites
wp site list

# Run command on specific site
wp option get blogname --url=https://subsite.example.com

# Run command on all sites
wp site list --field=url | xargs -I {} wp option get blogname --url={}

# Network-wide plugin activation
wp plugin activate plugin-name --network
```

### 7) Automation with wp-cli.yml

Create `wp-cli.yml` in site root:

```yaml
path: /path/to/wordpress
url: https://example.com
user: admin

# Environment-specific
@staging:
  url: https://staging.example.com

@production:
  url: https://example.com
  ssh: user@server/path/to/wordpress
```

Usage:

```bash
wp @staging plugin list
wp @production cache flush
```

## Verification

- Confirm intended side effects occurred
- Check URLs are correct after search-replace
- Verify plugins/themes in expected state
- Run health check if available: `wp doctor check`

## Failure modes / debugging

**"Error: This does not seem to be a WordPress installation"**
- Wrong `--path`
- Missing `wp-config.php`

**Multisite commands affecting wrong site**
- Missing or wrong `--url`

**Search-replace causing serialization issues**
- Use `--precise` flag
- Don't replace with different length strings in serialized data without `--recurse-objects`

## Escalation

- If you cannot confirm environment safety, do not run write operations
- For production changes, always backup first
- Document all commands run for audit trail
