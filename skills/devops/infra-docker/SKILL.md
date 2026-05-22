---
name: infra-docker
description: Local development environment with Docker Compose for PostgreSQL and other services. This skill should be used when setting up local infrastructure, managing development databases, or configuring containerized services.
---

# Docker Local Development Skill

Docker Compose patterns for local development environments including PostgreSQL and supporting services.

## When to Use This Skill

- Setting up local PostgreSQL for development
- Managing development databases
- Adding local services (Redis, etc.)
- Standardizing team development environments

## Quick Start

### Minimal Setup (PostgreSQL Only)

Create `docker-compose.yml` in project root:

```yaml
services:
  postgres:
    image: postgres:16-alpine
    container_name: myapp-postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: myapp
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

### Commands

```bash
# Start services
docker compose up -d

# View logs
docker compose logs -f postgres

# Stop services
docker compose down

# Stop and remove volumes (reset database)
docker compose down -v

# Check status
docker compose ps
```

## Environment Variables

### .env.local

```bash
# Database
DATABASE_URL=postgres://postgres:postgres@localhost:5432/myapp
```

### docker-compose.yml with .env file

```yaml
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-postgres}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-postgres}
      POSTGRES_DB: ${POSTGRES_DB:-myapp}
    ports:
      - "${POSTGRES_PORT:-5432}:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## Extended Setup

### PostgreSQL + Redis

```yaml
services:
  postgres:
    image: postgres:16-alpine
    container_name: myapp-postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: myapp
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: myapp-redis
    restart: unless-stopped
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
  redis_data:
```

### With pgAdmin (Database GUI)

```yaml
services:
  postgres:
    image: postgres:16-alpine
    container_name: myapp-postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: myapp
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  pgadmin:
    image: dpage/pgadmin4:latest
    container_name: myapp-pgadmin
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@local.dev
      PGADMIN_DEFAULT_PASSWORD: admin
      PGADMIN_CONFIG_SERVER_MODE: "False"
    ports:
      - "5050:80"
    volumes:
      - pgadmin_data:/var/lib/pgadmin
    depends_on:
      - postgres

volumes:
  postgres_data:
  pgadmin_data:
```

Access pgAdmin at http://localhost:5050

### With Minio (S3-Compatible Storage)

```yaml
services:
  minio:
    image: minio/minio:latest
    container_name: myapp-minio
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    ports:
      - "9000:9000"  # API
      - "9001:9001"  # Console
    volumes:
      - minio_data:/data

volumes:
  minio_data:
```

Access Minio Console at http://localhost:9001

## Database Operations

### Connect with psql

```bash
# Using Docker
docker compose exec postgres psql -U postgres -d myapp

# Direct connection (if psql installed locally)
psql postgres://postgres:postgres@localhost:5432/myapp
```

### Common psql Commands

```sql
-- List databases
\l

-- Connect to database
\c myapp

-- List tables
\dt

-- Describe table
\d user

-- Show table data
SELECT * FROM "user" LIMIT 10;

-- Exit
\q
```

### Backup and Restore

```bash
# Backup
docker compose exec postgres pg_dump -U postgres myapp > backup.sql

# Restore
docker compose exec -T postgres psql -U postgres myapp < backup.sql

# Backup specific tables
docker compose exec postgres pg_dump -U postgres -t user -t session myapp > users_backup.sql
```

### Reset Database

```bash
# Drop and recreate
docker compose exec postgres psql -U postgres -c "DROP DATABASE IF EXISTS myapp;"
docker compose exec postgres psql -U postgres -c "CREATE DATABASE myapp;"

# Or restart with fresh volume
docker compose down -v
docker compose up -d
```

## Package.json Scripts

Add convenient scripts:

```json
{
  "scripts": {
    "docker:up": "docker compose up -d",
    "docker:down": "docker compose down",
    "docker:reset": "docker compose down -v && docker compose up -d",
    "docker:logs": "docker compose logs -f",
    "docker:psql": "docker compose exec postgres psql -U postgres -d myapp",
    "db:generate": "drizzle-kit generate",
    "db:migrate": "tsx src/lib/db/migrate.ts",
    "db:studio": "drizzle-kit studio",
    "dev": "next dev",
    "dev:full": "docker compose up -d && next dev"
  }
}
```

## Development Workflow

### Daily Workflow

```bash
# Start services (if not running)
npm run docker:up

# Run migrations (if schema changed)
npm run db:migrate

# Start dev server
npm run dev
```

### After Schema Changes

```bash
# Generate migration
npm run db:generate

# Apply migration
npm run db:migrate

# Verify in Drizzle Studio
npm run db:studio
```

### Fresh Start

```bash
# Reset everything
npm run docker:reset

# Run migrations
npm run db:migrate
```

## Health Checks

### Verify Services Running

```bash
# Check container status
docker compose ps

# Expected output:
# NAME              STATUS
# myapp-postgres    Up (healthy)
# myapp-redis       Up (healthy)
```

### Wait for Database

Script to wait for PostgreSQL before running commands:

```bash
#!/bin/bash
# wait-for-db.sh

echo "Waiting for PostgreSQL..."
until docker compose exec postgres pg_isready -U postgres > /dev/null 2>&1; do
  sleep 1
done
echo "PostgreSQL is ready!"
```

## Troubleshooting

### Port Already in Use

```bash
# Find what's using port 5432
lsof -i :5432

# Kill the process or use a different port
# In docker-compose.yml:
ports:
  - "5433:5432"  # Map to different local port
```

### Container Won't Start

```bash
# Check logs
docker compose logs postgres

# Common issues:
# - Port conflict: change port mapping
# - Volume permissions: docker compose down -v
# - Image pull failed: docker compose pull
```

### Connection Refused

```bash
# Verify container is running
docker compose ps

# Verify port mapping
docker compose port postgres 5432

# Test connection
docker compose exec postgres pg_isready -U postgres
```

### Slow Startup

```bash
# Pre-pull images
docker compose pull

# Check disk space
docker system df

# Clean up unused resources
docker system prune
```

## Gitignore

Add to `.gitignore`:

```
# Docker volumes (if not using named volumes)
.docker-data/

# Local environment overrides
docker-compose.override.yml
```

## Production Considerations

This setup is for **local development only**. For production:

- Use managed database services (AWS RDS, Aurora, etc.)
- Never use default passwords
- Configure proper networking and security groups
- Set up backups and monitoring
- See `infra-aws` skill for production deployment

## Quick Reference

| Command | Purpose |
|---------|---------|
| `docker compose up -d` | Start services |
| `docker compose down` | Stop services |
| `docker compose down -v` | Stop and reset data |
| `docker compose logs -f` | View logs |
| `docker compose ps` | Check status |
| `docker compose exec postgres psql -U postgres` | Connect to DB |
