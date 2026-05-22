---
name: dokploy-management
description: |
  Use when deploying, managing, or troubleshooting Dokploy instances via the CLI (https://github.com/Dokploy/cli).
  Triggers: "dokploy deploy", "manage dokploy", "dokploy app", "dokploy database", "push to dokploy",
  "dokploy CI/CD", "dokploy authentication", "zero-downtime deployment", "dokploy docker-compose",
  "dokploy environment variables", "dokploy health checks".
  Provides comprehensive workflows for authentication, project/app/database management, environment variable
  sync, and production-ready CI/CD patterns with GitHub Actions.
---

# Dokploy Management

Comprehensive guide for managing Dokploy instances via CLI, API, and production deployment patterns.

## CLI Options

This skill includes **two CLI options**:

| CLI | Coverage | Runtime | Best For |
|-----|----------|---------|----------|
| **Custom CLI** (`./cli/`) | ~90% of API | Deno (single binary) | Full control, CI/CD, automation |
| **Official CLI** (`@dokploy/cli`) | ~8% of API | Node.js 18+ | Basic operations |

**Recommendation**: Use the custom CLI for comprehensive API access and zero-dependency deployment.

## Quick Reference (Custom CLI)

| Task | Command | Notes |
|------|---------|-------|
| **Authenticate** | `dokploy auth login --url <url> --token <token>` | Saves to `~/.config/dokploy/` |
| **Deploy app** | `dokploy app deploy <appId>` | No interactive prompts |
| **Create compose** | `dokploy compose create --name <n> --environment <id>` | Full compose support |
| **Manage domains** | `dokploy domain create --host <h> --app <id>` | SSL, paths, ports |
| **Database ops** | `dokploy db create postgres --name <n> --environment <id>` | All 5 DB types |
| **CI/CD** | `DOKPLOY_TOKEN=x dokploy app deploy <id>` | Env var auth |

## Installation

### Custom CLI (Recommended)

```bash
# Option 1: Run with Deno
deno run --allow-all ./cli/mod.ts [command]

# Option 2: Compile to binary
cd cli && deno task compile
./dist/dokploy --help

# Option 3: Install globally
deno install --allow-all -n dokploy ./cli/mod.ts
```

### Official CLI (Limited)

```bash
npm install -g @dokploy/cli
```

## Authentication

### Custom CLI

```bash
# Interactive
dokploy auth login --url https://panel.example.com --token YOUR_TOKEN

# Environment variables (CI/CD)
export DOKPLOY_URL="https://panel.example.com"
export DOKPLOY_TOKEN="YOUR_TOKEN"

# Check status
dokploy auth status
```

### Config File Location

`~/.config/dokploy/config.json`:
```json
{
  "url": "https://panel.example.com",
  "token": "your-token",
  "defaultProjectId": "optional",
  "defaultEnvironmentId": "optional"
}
```

## Core Workflows

### Workflow 1: Project Setup

```bash
# 1. Authenticate
dokploy auth login --url https://panel.example.com --token TOKEN

# 2. Create project
dokploy project create --name "Production"

# 3. Get project details (includes environment IDs)
dokploy project get <projectId>

# 4. Create application
dokploy app create --name "web-app" --environment <envId>

# 5. Set environment variables
dokploy app env <appId> --file .env.production

# 6. Deploy
dokploy app deploy <appId>
```

### Workflow 2: Docker Compose Stack

```bash
# Create compose stack (defaults to sourceType=github, must change to raw)
dokploy compose create \
  --name "full-stack" \
  --environment <envId> \
  --file docker-compose.yml

# IMPORTANT: Set source type to "raw" for direct compose files
# (Use API client or Deno script - see "Compose Source Types" section below)

# Set environment variables for the compose stack
# (Use API client - env vars go in compose.update with "env" field)

# Deploy
dokploy compose deploy <composeId>

# Add domain (pointing to specific service)
dokploy domain create \
  --host app.example.com \
  --compose <composeId> \
  --service web \
  --https \
  --port 80

# IMPORTANT: Redeploy after adding domain for Traefik to pick up the route
dokploy compose deploy <composeId>
```

### Workflow 3: Database Setup

```bash
# Create PostgreSQL
dokploy db create postgres \
  --name "Production DB" \
  --environment <envId> \
  --db-name myapp \
  --db-user postgres \
  --db-password "$DB_PASSWORD"

# Deploy
dokploy db deploy postgres <postgresId>

# Supported: postgres, mysql, mariadb, mongo, redis
```

### Workflow 4: Domain Configuration

```bash
# Create HTTPS domain with Let's Encrypt
dokploy domain create \
  --host api.example.com \
  --app <appId> \
  --https \
  --cert letsencrypt

# Generate traefik.me domain (for testing)
dokploy domain generate --app-name myapp
```

### Workflow 5: CI/CD with GitHub Actions

```yaml
name: Deploy to Dokploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Deno
        uses: denoland/setup-deno@v2
        
      - name: Deploy
        env:
          DOKPLOY_URL: ${{ secrets.DOKPLOY_URL }}
          DOKPLOY_TOKEN: ${{ secrets.DOKPLOY_TOKEN }}
        run: |
          deno run --allow-all ./cli/mod.ts app deploy ${{ secrets.APP_ID }}
```

Or with direct API call:

```yaml
- name: Deploy to Dokploy
  run: |
    curl -X POST "${{ secrets.DOKPLOY_URL }}/api/application.deploy" \
      -H "x-api-key: ${{ secrets.DOKPLOY_TOKEN }}" \
      -H "Content-Type: application/json" \
      -d '{"applicationId": "${{ secrets.APP_ID }}"}'
```

## Command Reference (Custom CLI)

### Auth Commands

```bash
dokploy auth login --url <url> --token <token>
dokploy auth logout
dokploy auth status
dokploy auth set-default --project <id> --environment <id>
```

### Project Commands

```bash
dokploy project list
dokploy project get <projectId>
dokploy project create --name <name> [--description <desc>]
dokploy project delete <projectId> [--force]
```

### Application Commands

```bash
dokploy app get <appId>
dokploy app create --name <name> --environment <envId> [--app-name <slug>]
dokploy app deploy <appId> [--title <title>]
dokploy app redeploy <appId>
dokploy app start <appId>
dokploy app stop <appId>
dokploy app delete <appId> [--force]
dokploy app env <appId>                    # Get env vars
dokploy app env <appId> --set KEY=value    # Set env var
dokploy app env <appId> --file .env        # Set from file
```

### Compose Commands

```bash
dokploy compose get <composeId>
dokploy compose create --name <name> --environment <envId> [--file <path>] [--type docker-compose|stack]
dokploy compose deploy <composeId>
dokploy compose start <composeId>
dokploy compose stop <composeId>
dokploy compose delete <composeId> [--force]
dokploy compose file <composeId>           # Get compose file
dokploy compose file <composeId> --set <path>  # Update compose file
```

### Domain Commands

```bash
dokploy domain list --app <appId>
dokploy domain list --compose <composeId>
dokploy domain get <domainId>
dokploy domain create --host <host> --app <appId> [--https] [--port <port>] [--path <path>]
dokploy domain create --host <host> --compose <composeId> --service <name>
dokploy domain delete <domainId> [--force]
dokploy domain generate --app-name <name>
```

### Database Commands

```bash
# Supported types: postgres, mysql, mariadb, mongo, redis
dokploy db create <type> --name <name> --environment <envId> \
  [--db-name <name>] [--db-user <user>] [--db-password <pass>] [--image <image>]
dokploy db deploy <type> <databaseId>
dokploy db start <type> <databaseId>
dokploy db stop <type> <databaseId>
dokploy db delete <type> <databaseId> [--force]
```

### Server Commands

```bash
dokploy server list
dokploy server get <serverId>
dokploy server create --name <name> --ip <ip> --port <port> --user <user> --ssh-key <keyId> --type deploy|build
dokploy server validate <serverId>
dokploy server delete <serverId> [--force]
```

### Docker Commands

```bash
dokploy docker containers [--server <serverId>]
dokploy docker restart <containerId> [--server <serverId>]
```

## JSON Output

All commands support `--json` for machine-readable output:

```bash
dokploy project list --json | jq '.[].projectId'
dokploy app get abc123 --json > app-config.json
```

## API Reference

The custom CLI uses these API endpoints:

| Category | Endpoints | Coverage |
|----------|-----------|----------|
| Auth | `user.get` | ✅ |
| Projects | `project.all`, `project.one`, `project.create`, `project.remove` | ✅ |
| Applications | `application.*` (27 endpoints) | ✅ |
| Compose | `compose.*` (26 endpoints) | ✅ |
| Domains | `domain.*` (9 endpoints) | ✅ |
| Databases | `postgres.*`, `mysql.*`, `mariadb.*`, `mongo.*`, `redis.*` | ✅ |
| Servers | `server.*` (16 endpoints) | ✅ |
| Docker | `docker.*` (7 endpoints) | ✅ |

See `./cli/lib/client.ts` for the full typed API client.

## Important Gotchas

### Compose Source Types

When creating a compose stack, the default `sourceType` is `github`. For raw compose files (no git repo), you **must** update to `sourceType: "raw"`:

```typescript
// Using the API client directly (Deno)
import { DokployClient } from "./cli/lib/client.ts";
const client = await DokployClient.create();

// Update source type to raw
await client.updateCompose("<composeId>", { sourceType: "raw" });

// Set environment variables
await client.updateCompose("<composeId>", { 
  env: `VAR1=value1
VAR2=value2` 
});
```

Without this, deployment will fail with "Github Provider not found".

### Compose File Compatibility

Dokploy does **NOT** support `env_file` directive in docker-compose.yml. You must:
1. Inline all environment variables in the `environment` section
2. Use YAML anchors (`&anchor` / `*anchor`) for shared env vars
3. Set sensitive values via Dokploy's env var system (compose.update with `env` field)

**Before (won't work)**:
```yaml
services:
  app:
    env_file:
      - .env
```

**After (works)**:
```yaml
services:
  app:
    environment:
      DB_HOST: "${DB_HOST}"
      DB_PASS: "${DB_PASS}"
```

### Domain + Deploy Order

After adding a domain to an application or compose stack, you **must redeploy** for Traefik to pick up the new routing:

```bash
dokploy domain create --host example.com --compose <id> --service web --https
dokploy compose deploy <id>  # Required!
```

### Network Requirements

All services must be on `dokploy-network` (external) to be routable:

```yaml
services:
  web:
    networks:
      - dokploy-network

networks:
  dokploy-network:
    external: true
```

## Troubleshooting

### Authentication Issues

```bash
# Check current auth
dokploy auth status

# Re-authenticate
dokploy auth login --url https://... --token ...

# Verify environment variables are set
env | grep DOKPLOY
```

### Deployment Failures

1. Check application/compose status: `dokploy compose get <id>` or `dokploy app get <id>`
2. Check deployment history via API for error messages
3. Common errors:
   - **"Github Provider not found"** → Set `sourceType: "raw"` for direct compose files
   - **"env_file not found"** → Inline env vars, Dokploy doesn't support env_file
   - **Container not routing** → Ensure service is on `dokploy-network` and redeploy after adding domain
4. Verify health endpoint responds
5. Check Dokploy web UI for deployment logs
6. Ensure `dokploy-network` exists: `docker network ls`

### Missing IDs

Run list commands to find IDs:
```bash
dokploy project list --json | jq '.[] | {id: .projectId, name: .name}'
dokploy project get <projectId> --json | jq '.environments[] | {id: .environmentId, name: .name}'
```

## Resources

- **Custom CLI**: `./cli/` directory in this skill
- **Official CLI**: https://github.com/Dokploy/cli
- **Official Docs**: https://docs.dokploy.com
- **API Spec**: Available at `https://your-instance/api/settings.getOpenApiDocument`

## Example: Full Compose Deployment

Complete example deploying a multi-service app with database:

```bash
# 1. Create the compose stack
dokploy compose create --name "MyApp" --environment <envId> --file docker-compose.yml

# 2. Set source type to raw (required for direct compose files)
deno run --allow-all - <<'EOF'
import { DokployClient } from "./cli/lib/client.ts";
const client = await DokployClient.create();
await client.updateCompose("<composeId>", { 
  sourceType: "raw",
  env: `DB_PASSWORD=secretpass123
REDIS_URL=redis://redis:6379`
});
console.log("Updated!");
EOF

# 3. Deploy
dokploy compose deploy <composeId>

# 4. Verify containers are running
dokploy docker containers | grep <app-name>

# 5. Add domain
dokploy domain create --host myapp.example.com --compose <composeId> --service web --https --port 80

# 6. Redeploy to apply domain routing
dokploy compose deploy <composeId>

# 7. Verify
curl https://myapp.example.com/health
```
