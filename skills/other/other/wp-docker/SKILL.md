---
name: wp-docker
description: Docker-based WordPress development environment. Use when setting up new WordPress sites, managing Docker containers, or automating site deployment with WP-CLI.
allowed-tools: Bash, Read, Write, Edit, Task
---

# WordPress Docker Environment Skill

Complete Docker Compose setup for WordPress development with WP-CLI automation.

## Quick Start

```bash
# Navigate to project directory
cd /path/to/project

# Copy templates
cp ~/.claude/skills/wp-docker/templates/* .

# Start environment
docker-compose up -d

# Run setup script
./wp-setup.sh "http://localhost:8080" "Site Name" "admin" "password" "admin@example.com"
```

---

## Docker Compose Stack

### Services

| Service | Image | Purpose | Port |
|---------|-------|---------|------|
| `db` | mariadb:10.11 | MySQL database | 3306 (internal) |
| `wordpress` | wordpress:php8.3-apache | WordPress + Apache | 8080 |
| `wpcli` | wordpress:cli | WP-CLI commands | - |

### Volume Mounts

| Host Path | Container Path | Purpose |
|-----------|----------------|---------|
| `./wp-content` | `/var/www/html/wp-content` | Themes, plugins, uploads |
| `db_data` | `/var/lib/mysql` | Database persistence |
| `./uploads.ini` | `/usr/local/etc/php/conf.d/uploads.ini` | PHP config |

---

## WP-CLI Commands

### Site Installation

```bash
# Install WordPress
docker-compose run --rm wpcli core install \
  --url="http://localhost:8080" \
  --title="Site Name" \
  --admin_user="admin" \
  --admin_password="password" \
  --admin_email="admin@example.com"
```

### Plugin Management

```bash
# Install and activate plugins
docker-compose run --rm wpcli plugin install \
  admin-site-enhancements \
  branda-white-labeling \
  admin-menu-editor \
  yoast-seo \
  litespeed-cache \
  ewww-image-optimizer \
  wp-mail-smtp \
  instant-images \
  --activate

# List installed plugins
docker-compose run --rm wpcli plugin list

# Update all plugins
docker-compose run --rm wpcli plugin update --all
```

### Theme Management

```bash
# Install and activate theme
docker-compose run --rm wpcli theme install theme-name --activate

# List themes
docker-compose run --rm wpcli theme list
```

### Content Creation

```bash
# Create page
docker-compose run --rm wpcli post create \
  --post_type=page \
  --post_title="About Us" \
  --post_status=publish

# Create post
docker-compose run --rm wpcli post create \
  --post_type=post \
  --post_title="Hello World" \
  --post_content="Welcome to our site." \
  --post_status=publish
```

### Options Management

```bash
# Update site options
docker-compose run --rm wpcli option update blogname "Site Name"
docker-compose run --rm wpcli option update blogdescription "Site tagline"
docker-compose run --rm wpcli option update permalink_structure '/%postname%/'

# Configure ASE
docker-compose run --rm wpcli option update admin_site_enhancements \
  '{"change_login_url":{"enabled":true,"slug":"secure-login"}}' \
  --format=json
```

### Database Operations

```bash
# Export database
docker-compose run --rm wpcli db export backup.sql

# Import database
docker-compose run --rm wpcli db import backup.sql

# Search and replace (for migrations)
docker-compose run --rm wpcli search-replace "old-domain.com" "new-domain.com"
```

---

## Environment Commands

### Start/Stop

```bash
# Start containers
docker-compose up -d

# Stop containers
docker-compose down

# Stop and remove volumes (DESTRUCTIVE)
docker-compose down -v

# View logs
docker-compose logs -f wordpress

# Restart WordPress
docker-compose restart wordpress
```

### Health Checks

```bash
# Check running containers
docker-compose ps

# Check WordPress version
docker-compose run --rm wpcli core version

# Check database connection
docker-compose run --rm wpcli db check
```

---

## Common Workflows

### New Site Setup

1. Copy templates to project directory
2. Start Docker environment
3. Run wp-setup.sh script
4. Configure white-labeling
5. Create initial pages
6. Run SEO setup

### Site Migration

```bash
# Export from source
docker-compose run --rm wpcli db export backup.sql

# Copy wp-content folder

# Import to destination
docker-compose run --rm wpcli db import backup.sql

# Update URLs
docker-compose run --rm wpcli search-replace "old-url.com" "new-url.com"

# Flush cache
docker-compose run --rm wpcli cache flush
```

### Plugin Audit

```bash
# List plugins with updates available
docker-compose run --rm wpcli plugin list --update=available

# Check for security issues
docker-compose run --rm wpcli plugin verify-checksums --all
```

---

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs db
docker-compose logs wordpress

# Rebuild containers
docker-compose up -d --build
```

### Database Connection Failed

```bash
# Wait for database to be ready
docker-compose exec db mysqladmin ping -h localhost -u root -p

# Check environment variables
docker-compose config
```

### Permission Issues

```bash
# Fix wp-content permissions
docker-compose exec wordpress chown -R www-data:www-data /var/www/html/wp-content
```

### WP-CLI Not Working

```bash
# Run with shell access
docker-compose run --rm --entrypoint /bin/sh wpcli

# Check WordPress installation
docker-compose run --rm wpcli core is-installed
```

---

## PHP Configuration

### uploads.ini

```ini
upload_max_filesize = 64M
post_max_size = 64M
max_execution_time = 300
memory_limit = 256M
```

---

## Related Skills

- **white-label**: Configure ASE + Branda for admin branding
- **wordpress-admin**: REST API and content management
- **wp-performance**: LiteSpeed Cache and optimization
- **seo-optimizer**: Yoast SEO configuration

---

## Templates Location

All templates are in: `~/.claude/skills/wp-docker/templates/`

- `docker-compose.yml` - Full stack configuration
- `wp-setup.sh` - Automated site setup script
- `uploads.ini` - PHP configuration
- `.env.example` - Environment variables template
