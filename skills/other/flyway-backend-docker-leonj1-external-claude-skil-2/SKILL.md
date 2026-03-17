---
name: flyway-backend-docker
description: Setup backend project with Flyway SQL migrations, tini init system, and MySQL integration testing. Modifies existing Dockerfile from backend-docker skill.
depends_on: [backend-docker]
---

# Flyway Backend Docker Skill

This skill configures a backend project to use Flyway for SQL schema management. It **modifies an existing Dockerfile** (created by the `backend-docker` skill) to add tini as init system and Flyway migrations that run before the application starts.

## Prerequisites

- **backend-docker skill must be applied first** - A Dockerfile must already exist
- Docker installed and running
- MySQL or compatible database will be used

## When to Invoke This Skill

Invoke this skill when ANY of these conditions are true:

1. **User asks for Flyway setup**: "add flyway", "setup flyway migrations", "database migrations with flyway"
2. **User needs SQL schema management**: "manage database schema", "SQL migrations"
3. **User wants tini + flyway in Docker**: "run migrations before app starts"
4. **Backend needs MySQL with migrations**: "setup mysql with migrations"

## Workflow

### Step 1: Verify Dockerfile Exists

```bash
# Check for existing Dockerfile (from backend-docker skill)
ls ${BACKEND_PATH}/Dockerfile
```

If Dockerfile does not exist, invoke the `backend-docker` skill first.

### Step 2: Create SQL Directory Structure

Create the `./sql` directory with the AGENTS.md file:

```bash
mkdir -p ${BACKEND_PATH}/sql
```

Create `${BACKEND_PATH}/sql/AGENTS.md`:

```markdown
# SQL Migrations Directory

This folder contains Flyway SQL migration files.

## IMPORTANT: Agent Rules

**DO NOT** modify or delete any existing files in this folder.

**ONLY** add new migration files following the Flyway naming convention:
- `V{version}__{description}.sql` for versioned migrations
- `U{version}__{description}.sql` for undo migrations (optional)
- `R__{description}.sql` for repeatable migrations

### Naming Convention Examples

- `V1__create_users_table.sql`
- `V2__add_email_to_users.sql`
- `V3__create_orders_table.sql`
- `R__refresh_views.sql`

### Why This Restriction?

Flyway tracks applied migrations by checksum. Modifying an already-applied migration will cause:
- Migration failures
- Checksum mismatch errors
- Database inconsistency

If you need to change existing schema, create a NEW migration file with the next version number.
```

### Step 3: Create Hello World Migration

Create `${BACKEND_PATH}/sql/V1__hello_world.sql`:

```sql
-- Flyway Hello World Migration
-- This validates that Flyway is correctly configured

CREATE TABLE IF NOT EXISTS flyway_hello_world (
    id INT AUTO_INCREMENT PRIMARY KEY,
    message VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO flyway_hello_world (message) VALUES ('Hello from Flyway!');
```

### Step 4: Create Entrypoint Script

Create `${BACKEND_PATH}/docker-entrypoint.sh`:

```bash
#!/bin/sh
set -e

echo "=== Running Flyway migrations ==="

# Wait for database to be ready
until nc -z -v -w30 ${DB_HOST:-db} ${DB_PORT:-3306}
do
  echo "Waiting for database connection at ${DB_HOST:-db}:${DB_PORT:-3306}..."
  sleep 2
done

echo "Database is up - running migrations"

# Run Flyway migrations
flyway -url="jdbc:mysql://${DB_HOST:-db}:${DB_PORT:-3306}/${DB_NAME:-app}?allowPublicKeyRetrieval=true&useSSL=false" \
       -user=${DB_USER:-root} \
       -password=${DB_PASSWORD:-root} \
       -locations=filesystem:/app/sql \
       -connectRetries=5 \
       migrate

echo "=== Flyway migrations complete ==="
echo "=== Starting application ==="

# Execute the main command (passed as arguments)
exec "$@"
```

### Step 5: Modify Existing Dockerfile

Read the existing Dockerfile and apply these modifications:

#### 5a: Add Flyway Dependencies

**For Debian/Ubuntu-based images** (python:*-slim, etc.), add after existing apt-get install:

```dockerfile
# Install tini, flyway dependencies, and netcat for health checks
RUN apt-get update && apt-get install -y --no-install-recommends \
    tini \
    curl \
    netcat-openbsd \
    default-jre-headless \
    && rm -rf /var/lib/apt/lists/*
```

**For Alpine-based images** (node:*-alpine, golang:*-alpine, etc.), add:

```dockerfile
# Install tini and dependencies for flyway
RUN apk add --no-cache tini openjdk17-jre-headless curl bash netcat-openbsd
```

#### 5b: Add Flyway Installation

Add after the dependency installation:

```dockerfile
# Install Flyway
ENV FLYWAY_VERSION=10.22.0
RUN mkdir -p /tmp/flyway && \
    curl -fSL --retry 3 --retry-delay 5 \
        "https://repo1.maven.org/maven2/org/flywaydb/flyway-commandline/${FLYWAY_VERSION}/flyway-commandline-${FLYWAY_VERSION}-linux-x64.tar.gz" \
        -o /tmp/flyway/flyway.tar.gz && \
    tar -xzf /tmp/flyway/flyway.tar.gz -C /opt && \
    ln -s /opt/flyway-${FLYWAY_VERSION}/flyway /usr/local/bin/flyway && \
    rm -rf /tmp/flyway
```

**Note**: For Alpine images, use `linux-alpine-x64.tar.gz` instead of `linux-x64.tar.gz`.

#### 5c: Add SQL and Entrypoint Copies

Add before `COPY . .`:

```dockerfile
# Copy SQL migrations
COPY sql/ /app/sql/

# Copy entrypoint
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
```

#### 5d: Modify ENTRYPOINT and CMD

Replace the existing CMD with ENTRYPOINT + CMD pattern:

**For Debian-based images:**
```dockerfile
ENTRYPOINT ["/usr/bin/tini", "--", "/docker-entrypoint.sh"]
CMD ["<original-cmd>"]
```

**For Alpine-based images:**
```dockerfile
ENTRYPOINT ["/sbin/tini", "--", "/docker-entrypoint.sh"]
CMD ["<original-cmd>"]
```

Where `<original-cmd>` is the original CMD from the Dockerfile (e.g., `python -m uvicorn app.main:app --host 0.0.0.0 --port 8000`).

### Step 6: Create docker-compose.yml for Testing

Create `${BACKEND_PATH}/docker-compose.yml`:

```yaml
services:
  db:
    image: mysql:8.0
    container_name: flyway-test-db
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: app
      MYSQL_USER: appuser
      MYSQL_PASSWORD: apppassword
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u", "root", "-proot"]
      interval: 5s
      timeout: 5s
      retries: 10
      start_period: 30s

  app:
    build: .
    container_name: flyway-test-app
    environment:
      DB_HOST: db
      DB_PORT: 3306
      DB_NAME: app
      DB_USER: root
      DB_PASSWORD: root
    ports:
      - "8080:8080"
    depends_on:
      db:
        condition: service_healthy

volumes:
  mysql_data:
```

### Step 7: Create Integration Test Script

Create `${BACKEND_PATH}/test-flyway-integration.sh`:

```bash
#!/bin/bash
set -e

echo "=== Flyway Integration Test ==="

# Cleanup any existing containers
docker compose down -v 2>/dev/null || true

# Start MySQL
echo "Starting MySQL container..."
docker compose up -d db

# Wait for MySQL to be healthy
echo "Waiting for MySQL to be ready..."
timeout=90
while [ $timeout -gt 0 ]; do
    if docker compose exec -T db mysqladmin ping -h localhost -u root -proot 2>/dev/null; then
        echo "MySQL is ready!"
        break
    fi
    echo "Waiting... ($timeout seconds remaining)"
    sleep 2
    timeout=$((timeout - 2))
done

if [ $timeout -le 0 ]; then
    echo "ERROR: MySQL failed to start within timeout"
    docker compose logs db
    docker compose down -v
    exit 1
fi

# Build and start app (which runs Flyway migrations)
echo "Building and starting app container..."
docker compose up -d --build app

# Wait for app to start and run migrations
echo "Waiting for app to start..."
sleep 15

# Check if app is running
if ! docker compose ps app | grep -q "Up"; then
    echo "ERROR: App container failed to start"
    docker compose logs app
    docker compose down -v
    exit 1
fi

# Verify Flyway migration was applied
echo "Verifying Flyway migration..."
RESULT=$(docker compose exec -T db mysql -u root -proot -D app -e "SELECT message FROM flyway_hello_world LIMIT 1;" 2>/dev/null)

if echo "$RESULT" | grep -q "Hello from Flyway!"; then
    echo "SUCCESS: Flyway migration applied correctly!"
    echo "Found message: Hello from Flyway!"
else
    echo "ERROR: Flyway migration verification failed"
    echo "Query result: $RESULT"
    docker compose logs app
    docker compose down -v
    exit 1
fi

# Cleanup
echo "Cleaning up..."
docker compose down -v

echo "=== Integration Test PASSED ==="
```

### Step 8: Validate Setup

Run the integration test:

```bash
cd ${BACKEND_PATH}
chmod +x test-flyway-integration.sh docker-entrypoint.sh
./test-flyway-integration.sh
```

Expected output:
- MySQL container starts successfully
- App container builds and starts
- Flyway migrations run without errors
- `flyway_hello_world` table contains "Hello from Flyway!"

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| DB_HOST | db | Database hostname |
| DB_PORT | 3306 | Database port |
| DB_NAME | app | Database name |
| DB_USER | root | Database user |
| DB_PASSWORD | root | Database password |

## Adding New Migrations

To add a new migration:

```bash
# Create new migration file
touch sql/V2__create_users_table.sql
```

**IMPORTANT**: Never modify existing migration files. Always create new versioned migrations.

## Error Handling

### Flyway Migration Fails

1. Check database connectivity: Verify `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`
2. Check SQL syntax: Review migration files for errors
3. Check Flyway logs: `docker compose logs app`

### Tini Not Found

1. Verify tini is installed in Dockerfile
2. Check path: Alpine uses `/sbin/tini`, Debian uses `/usr/bin/tini`

### Database Connection Timeout

1. Increase wait time in `docker-entrypoint.sh`
2. Check MySQL healthcheck in docker-compose.yml

## Do NOT Invoke When

- Project doesn't need SQL schema management
- Project uses a different migration tool (Liquibase, Alembic, etc.)
- Project doesn't use a relational database
- Dockerfile doesn't exist (invoke backend-docker first)
