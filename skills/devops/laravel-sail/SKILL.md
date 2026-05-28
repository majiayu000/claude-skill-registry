---
name: laravel-sail
description: >-
  Develops with Laravel Sail Docker environment. Activates when working with Docker containers,
  Sail commands, adding services (MySQL, Redis, Meilisearch), or when user mentions Sail, Docker,
  container, sail up, or development environment.
---

# Laravel Sail Development

## When to Apply

Activate this skill when:

- Starting or stopping the Docker environment
- Adding services to Sail (MySQL, Redis, etc.)
- Running commands inside containers
- Debugging container issues
- Configuring Docker services

## Documentation

Use `search-docs` for detailed Laravel Sail patterns and documentation.

## Basic Commands

### Starting and Stopping

```bash
# Start all containers
./vendor/bin/sail up

# Start in background (detached)
./vendor/bin/sail up -d

# Stop containers
./vendor/bin/sail down

# Stop and remove volumes (reset databases)
./vendor/bin/sail down -v
```

### Running Commands

```bash
# Run Artisan commands
./vendor/bin/sail artisan migrate

# Run Composer
./vendor/bin/sail composer require package/name

# Run NPM
./vendor/bin/sail npm install
./vendor/bin/sail npm run dev

# Run tests
./vendor/bin/sail test

# Run Tinker
./vendor/bin/sail tinker
```

### Shell Access

```bash
# Access application container shell
./vendor/bin/sail shell

# Run command as root
./vendor/bin/sail root-shell
```

## Adding Services

```bash
# Add services interactively
php artisan sail:add

# Or specify services
php artisan sail:add mysql redis meilisearch
```

### Available Services

- MySQL 8.0
- PostgreSQL
- MariaDB
- Redis
- Memcached
- Meilisearch
- Typesense
- MinIO
- Mailpit
- Selenium

## Configuration

### docker-compose.yml

<code-snippet name="Custom Service" lang="yaml">
# docker-compose.yml
services:
    laravel.test:
        build:
            context: ./vendor/laravel/sail/runtimes/8.3
            dockerfile: Dockerfile
        ports:
            - '${APP_PORT:-80}:80'
        environment:
            WWWUSER: '${WWWUSER}'
            LARAVEL_SAIL: 1
        volumes:
            - '.:/var/www/html'
        networks:
            - sail
        depends_on:
            - mysql
            - redis
</code-snippet>

### Environment Variables

<code-snippet name="Sail Environment" lang="env">
# .env
APP_PORT=80
FORWARD_DB_PORT=3306
FORWARD_REDIS_PORT=6379

# Database connection
DB_CONNECTION=mysql
DB_HOST=mysql
DB_PORT=3306
DB_DATABASE=laravel
DB_USERNAME=sail
DB_PASSWORD=password

# Redis
REDIS_HOST=redis
REDIS_PASSWORD=null
REDIS_PORT=6379
</code-snippet>

## Sail Alias

Add to your shell profile for convenience:

```bash
# ~/.bashrc or ~/.zshrc
alias sail='[ -f sail ] && sh sail || sh vendor/bin/sail'
```

Then use:

```bash
sail up -d
sail artisan migrate
sail npm run dev
```

## Database Access

```bash
# MySQL CLI
./vendor/bin/sail mysql

# PostgreSQL CLI
./vendor/bin/sail psql

# Redis CLI
./vendor/bin/sail redis
```

## Debugging

```bash
# View container logs
./vendor/bin/sail logs

# View specific service logs
./vendor/bin/sail logs mysql

# Follow logs
./vendor/bin/sail logs -f
```

### Xdebug

<code-snippet name="Enable Xdebug" lang="env">
# .env
SAIL_XDEBUG_MODE=develop,debug
SAIL_XDEBUG_CONFIG="client_host=host.docker.internal"
</code-snippet>

## Publishing Sail Files

```bash
# Publish docker-compose.yml and Dockerfiles
php artisan sail:publish
```

This allows customizing the Docker configuration.

## Common Pitfalls

- Forgetting to start Sail before running commands
- Using `localhost` instead of service names for connections (use `mysql` not `localhost`)
- Port conflicts with local services
- Not using `sail` prefix for commands (running `php artisan` instead of `sail artisan`)
- Volume permission issues (use `sail root-shell` to fix)
- Forgetting to rebuild after Dockerfile changes (`sail build --no-cache`)
