---
name: tg-deployment
description: Production deployment patterns for the World of Darkness Django application. Use when deploying to staging/production, configuring security settings, setting up Redis cache, planning database migrations, or preparing rollback procedures. Triggers on deployment tasks, production configuration, security hardening, or environment-specific settings.
---

# Deployment Patterns

## Environment Configuration

### Settings Structure

```
tg/settings/
├── __init__.py        # Auto-loads based on DJANGO_ENVIRONMENT
├── base.py            # Common settings (all environments)
├── development.py     # DEBUG=True, local cache
└── production.py      # Full security, Redis, HTTPS
```

Set `DJANGO_ENVIRONMENT=production` in `.env` for production.

### Required Production Environment Variables

```bash
# Critical - must be set
DJANGO_ENVIRONMENT=production
SECRET_KEY=<generated-secret-key>
DJANGO_ALLOWED_HOSTS=example.com,www.example.com
CSRF_TRUSTED_ORIGINS=https://example.com

# Database (PostgreSQL recommended)
DB_NAME=tg_db
DB_USER=tg_user
DB_PASSWORD=<secure-password>
DB_HOST=localhost
DB_PORT=5432

# Redis cache
REDIS_URL=redis://127.0.0.1:6379/1
```

Generate secret key: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`

## Security Configuration

### Production Security Settings (in production.py)

```python
# HTTPS enforcement
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HSTS (1 year)
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Content security
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"
SECURE_REFERRER_POLICY = "same-origin"

# Cookie security
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Strict"
```

Verify with: `python manage.py check --deploy`

## Redis Cache Setup

### Installation

```bash
pip install django-redis redis
```

### Configuration

```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get("REDIS_URL", "redis://127.0.0.1:6379/1"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 50},
            "RETRY_ON_TIMEOUT": True,
            "IGNORE_EXCEPTIONS": True,
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
        },
    }
}

# Session storage in Redis
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
```

### Verification

```python
from django.core.cache import cache
cache.set('test', 'value', 60)
cache.get('test')  # Should return 'value'
```

## Database Migration Deployment

### Pre-deployment

```bash
# Backup database
pg_dump production_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Validate existing data
python manage.py validate_data_integrity --verbose
python manage.py validate_data_integrity --fix  # If issues found
```

### Deployment Steps

```bash
# 1. Enable maintenance mode
touch /var/www/tg/maintenance.flag

# 2. Pull code
git fetch origin && git checkout <branch> && git pull

# 3. Install dependencies
pip install -r requirements.txt --upgrade

# 4. Run migrations
python manage.py showmigrations  # Preview
python manage.py migrate

# 5. Collect static
python manage.py collectstatic --noinput

# 6. Restart services
sudo systemctl restart gunicorn
sudo systemctl restart nginx

# 7. Disable maintenance mode
rm /var/www/tg/maintenance.flag
```

### Post-deployment

```bash
# Health check
curl -I https://your-domain.com/
python manage.py monitor_validation
```

## Rollback Procedures

### Code-only Rollback

```bash
git log --oneline  # Find previous commit
git checkout <previous-commit>
sudo systemctl restart gunicorn
```

### Full Rollback (Code + Database)

```bash
# 1. Stop application
sudo systemctl stop gunicorn

# 2. Restore database
dropdb production_db
createdb production_db
pg_restore -d production_db backup_TIMESTAMP.sql

# 3. Revert code
git checkout <previous-commit>
python manage.py migrate <app> <previous-migration>

# 4. Restart
sudo systemctl start gunicorn
```

## Deployment Checklist

### Pre-deployment
- [ ] All tests passing locally
- [ ] Database backup created and verified
- [ ] Rollback plan documented
- [ ] Team notified of deployment window

### During deployment
- [ ] Maintenance mode enabled
- [ ] Code pulled and dependencies updated
- [ ] Data validation passed
- [ ] Migrations applied successfully
- [ ] Static files collected
- [ ] Services restarted

### Post-deployment
- [ ] Health check passed
- [ ] Key functionality tested (login, create, edit)
- [ ] Error logs clean
- [ ] Maintenance mode disabled
- [ ] Monitor for 30 minutes

## Monitoring Commands

```bash
# Validation health check
python manage.py monitor_validation

# JSON output for monitoring tools
python manage.py monitor_validation --json

# Analyze specific time period
python manage.py monitor_validation --period 48
```
