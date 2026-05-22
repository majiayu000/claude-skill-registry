---
name: docker-makefile
description: Docker Compose orchestration and Makefile commands for the development environment. Use this skill when managing containers, debugging services, running make commands, or troubleshooting Docker issues.
---

# Docker & Makefile Skill

This skill provides guidance for managing the Family Plan development environment using Docker Compose and Makefile commands.

## Docker Services Overview

| Service | Port | Description |
|---------|------|-------------|
| `frontend` | 3000 | React development server |
| `nginx` | 8080 | Backend API reverse proxy |
| `php` | 9000 (internal) | PHP-FPM application server |
| `database` | 5432 | PostgreSQL database |
| `mailpit` | 8025 | Email testing UI |
| `node` | - | Asset builder (build only) |

## Essential Make Commands

### Service Management

```bash
# Start all services
make up

# Stop all services
make down

# Restart services
make restart

# View service status
docker compose ps

# Full cleanup (removes volumes)
make clean
```

### Initial Setup

```bash
# Complete project setup (first time)
make setup
# This runs: up -> install -> db-migrate -> create-admin

# Initialize development environment
make init

# Install all dependencies
make install
```

### Database Operations

```bash
# Run database migrations
make db-migrate

# Reset database (drop + create + migrate)
make db-reset

# Generate new migration from entity changes
make db-diff

# Direct database access
make shell-db
# Then: \dt to list tables, \d+ table_name for schema
```

### Testing

```bash
# Run all backend tests (PHPUnit + Behat)
make backend-test

# Run only PHPUnit tests
make phpunit

# Run only Behat acceptance tests
make behat

# Run frontend E2E tests
make frontend-test

# Run all tests
make test
```

### Shell Access

```bash
# PHP container shell
make shell-php
# or: make shell

# Database shell (psql)
make shell-db

# Frontend container shell
docker compose exec frontend sh
```

### Code Quality

```bash
# Run PHP linter (PHP-CS-Fixer)
make lint

# Auto-fix linting issues
make lint-fix
```

### Logs and Debugging

```bash
# All service logs
docker compose logs -f

# Specific service logs
docker compose logs -f php
docker compose logs -f frontend
docker compose logs -f database
docker compose logs -f nginx

# Last 100 lines
docker compose logs --tail=100 php
```

## Docker Compose Configuration

### compose.yaml Structure

```yaml
services:
  database:
    image: postgres:16-alpine
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: app
      POSTGRES_PASSWORD: "!ChangeMe!"
    volumes:
      - database_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "app"]
      interval: 10s
      timeout: 5s
      retries: 5

  php:
    build:
      context: .
      target: app_php_dev
    depends_on:
      database:
        condition: service_healthy
    volumes:
      - .:/srv/app
    environment:
      DATABASE_URL: postgresql://app:!ChangeMe!@database:5432/app

  nginx:
    build:
      context: .
      target: app_nginx
    depends_on:
      - php
    ports:
      - "8080:80"

  frontend:
    build:
      context: ./frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      - CHOKIDAR_USEPOLLING=true

  mailpit:
    image: axllent/mailpit
    ports:
      - "8025:8025"
      - "1025:1025"

volumes:
  database_data:
```

## Common Tasks

### Rebuilding Containers

```bash
# Rebuild all containers
docker compose build

# Rebuild specific service
docker compose build php

# Rebuild without cache
docker compose build --no-cache php

# Rebuild and restart
docker compose up -d --build
```

### Executing Commands in Containers

```bash
# Run command in PHP container
docker compose exec php <command>

# Examples:
docker compose exec php composer install
docker compose exec php php bin/console cache:clear
docker compose exec php vendor/bin/phpunit
docker compose exec php vendor/bin/behat

# Run command in frontend container
docker compose exec frontend npm install
docker compose exec frontend npm run build
```

### Database Management

```bash
# Create database backup
docker compose exec database pg_dump -U app app > backup.sql

# Restore database
docker compose exec -T database psql -U app app < backup.sql

# Run SQL query
docker compose exec database psql -U app -d app -c "SELECT * FROM users;"
```

### Clearing Caches

```bash
# Symfony cache
docker compose exec php php bin/console cache:clear

# Clear all caches (dev)
docker compose exec php php bin/console cache:clear --env=dev

# Clear Doctrine cache
docker compose exec php php bin/console doctrine:cache:clear-metadata
docker compose exec php php bin/console doctrine:cache:clear-query
docker compose exec php php bin/console doctrine:cache:clear-result
```

## Troubleshooting

### Service Won't Start

```bash
# Check logs for errors
docker compose logs php

# Verify dependencies are healthy
docker compose ps

# Restart specific service
docker compose restart php
```

### Database Connection Issues

```bash
# Check if database is ready
docker compose exec database pg_isready -U app

# Check database logs
docker compose logs database

# Reset database container
docker compose down -v  # WARNING: destroys data
docker compose up -d database
make db-migrate
```

### Permission Issues

```bash
# Fix file permissions (Linux)
sudo chown -R $(id -u):$(id -g) .

# In container
docker compose exec php chown -R www-data:www-data var/
```

### Port Conflicts

```bash
# Check what's using a port
lsof -i :8080
lsof -i :3000

# Stop conflicting service or change port in compose.yaml
```

### Memory Issues

```bash
# Check container resources
docker stats

# Increase Docker memory allocation in Docker Desktop settings
```

## Environment Variables

### Backend (.env)

```env
APP_ENV=dev
APP_SECRET=your-secret-key
DATABASE_URL="postgresql://app:!ChangeMe!@database:5432/app"
SUPER_ADMIN_EMAIL=admin@example.com
SUPER_ADMIN_PASSWORD=admin123
CORS_ALLOWED_ORIGIN=http://localhost:3000
MAILER_DSN=smtp://mailpit:1025
```

### Frontend (frontend/.env)

```env
REACT_APP_API_URL=http://localhost:8080
```

## Performance Tips

1. **Use named volumes** - Faster than bind mounts for dependencies
2. **Exclude node_modules** - Use anonymous volume to avoid syncing
3. **Enable BuildKit** - `DOCKER_BUILDKIT=1 docker compose build`
4. **Use .dockerignore** - Exclude unnecessary files from build context
5. **Health checks** - Ensure services start in correct order

## Quick Reference

| Task | Command |
|------|---------|
| Start environment | `make up` |
| Stop environment | `make down` |
| Run tests | `make test` |
| Database shell | `make shell-db` |
| PHP shell | `make shell-php` |
| View logs | `docker compose logs -f` |
| Run migrations | `make db-migrate` |
| Reset everything | `make clean && make setup` |
