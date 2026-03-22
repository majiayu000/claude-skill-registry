---
name: woo-deploy
description: Deploy WooCommerce — WP-CLI automation, database migrations, zero-downtime updates, staging workflows, environment configuration, and CI/CD patterns. Use when deploying WooCommerce stores or setting up deployment pipelines.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# WooCommerce Deployment

## Before writing code

**Fetch live docs**:
1. Fetch `https://developer.wordpress.org/cli/commands/` for WP-CLI reference
2. Web-search `woocommerce deployment best practices` for deployment patterns
3. Web-search `wordpress deployment ci cd` for CI/CD integration

## WP-CLI

### Essential WordPress Commands

| Command | Description |
|---------|-------------|
| `wp core update` | Update WordPress core |
| `wp plugin update --all` | Update all plugins |
| `wp plugin install <slug> --activate` | Install and activate plugin |
| `wp plugin deactivate <slug>` | Deactivate plugin |
| `wp db export backup.sql` | Export database |
| `wp db import backup.sql` | Import database |
| `wp cache flush` | Flush object cache |
| `wp rewrite flush` | Flush permalink rules |
| `wp search-replace <old> <new>` | Database search-replace (for migrations) |
| `wp cron event run --all` | Run all due cron events |

### WooCommerce-Specific Commands

| Command | Description |
|---------|-------------|
| `wp wc update` | Run WooCommerce database updates |
| `wp wc product list` | List products |
| `wp wc order list` | List orders |
| `wp wc customer list` | List customers |
| `wp wc setting list <group>` | View settings |
| `wp wc tool run <tool>` | Run WooCommerce tool (install_pages, etc.) |

### Scripted Deployment

```bash
# Deploy steps
wp maintenance-mode activate
wp db export pre-deploy-backup.sql
wp plugin update woocommerce
wp wc update                        # Run DB migrations
wp cache flush
wp rewrite flush
wp maintenance-mode deactivate
```

## Database Migrations

### WooCommerce Update Routine

When WooCommerce updates:
1. New version includes migration callbacks
2. `wp wc update` executes pending migrations
3. Migrations are versioned and idempotent
4. Track in `woocommerce_db_version` option

### Custom Extension Migrations

For your own plugin's schema changes:
- Store a `db_version` option
- On `plugins_loaded`, compare stored vs current version
- Run migration if needed using `dbDelta()` for CREATE/ALTER
- Update the stored version

### HPOS Migration

Migrate orders from posts to custom tables:
- WooCommerce > Settings > Advanced > Features
- Use the built-in migration tool (batched, resumable)
- Enable sync mode during transition
- Verify data integrity before switching authoritative source

## Environment Configuration

### wp-config.php Constants

| Constant | Purpose |
|----------|---------|
| `WP_DEBUG` | Enable debug mode |
| `WP_DEBUG_LOG` | Log errors to wp-content/debug.log |
| `SAVEQUERIES` | Log DB queries (dev only) |
| `WP_ENVIRONMENT_TYPE` | `local`, `development`, `staging`, `production` |
| `DISALLOW_FILE_EDIT` | Disable admin file editor |
| `DISALLOW_FILE_MODS` | Disable plugin/theme updates via admin |
| `FORCE_SSL_ADMIN` | Force HTTPS for admin |

### Environment Detection

`wp_get_environment_type()` returns the current environment type. Use for conditional behavior (debug output, test gateways, etc.).

## Staging & Production Workflow

### Recommended Flow

1. **Local** — develop and test
2. **Staging** — mirror production, final QA
3. **Production** — live store

### Database Migration Between Environments

- Export: `wp db export`
- Import: `wp db import`
- URL replacement: `wp search-replace 'https://staging.example.com' 'https://example.com' --all-tables`
- Always backup before replacing

### What NOT to Sync

- Active sessions and transients — they're environment-specific
- Payment gateway live keys (use environment-specific config)
- Email notification settings (avoid sending test emails from staging)

## CI/CD Patterns

### GitHub Actions / GitLab CI

Typical pipeline:
1. **Lint** — PHP_CodeSniffer with WPCS
2. **Unit Tests** — PHPUnit against WordPress test suite
3. **Integration Tests** — PHPUnit with WooCommerce loaded
4. **E2E Tests** — Playwright against test environment
5. **Deploy** — rsync/SSH or platform-specific deployer

### Deployment Methods

| Method | Description |
|--------|-------------|
| **Git-based** | Push to remote, server pulls (Bedrock/Trellis) |
| **rsync/SSH** | Sync files to server |
| **Platform CLI** | WP Engine, Pantheon, Kinsta, Flywheel |
| **Docker** | Build and deploy container images |
| **Composer** | Install/update via Composer on server |

## Maintenance Mode

- `wp maintenance-mode activate` — enable maintenance mode
- `wp maintenance-mode deactivate` — disable
- Or programmatic: create `.maintenance` file in WordPress root
- Custom maintenance page: `wp-content/maintenance.php`

## Best Practices

- Always backup before deploying (`wp db export`)
- Run `wp wc update` after WooCommerce version updates
- Use `wp search-replace` for URL changes between environments
- Set `WP_ENVIRONMENT_TYPE` per environment
- Disable file editing in production (`DISALLOW_FILE_EDIT`)
- Use maintenance mode during major updates
- Test updates on staging before production
- Automate deployments with CI/CD pipelines
- Keep deployment scripts in version control

Fetch the WP-CLI documentation and WordPress deployment guides for exact command syntax, flags, and platform-specific deployment patterns before implementing.
