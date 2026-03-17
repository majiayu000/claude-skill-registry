---
name: coder-convex-setup
description: Initial Convex workspace setup in Coder workspaces with self-hosted Convex deployment, authentication configuration, Docker setup, and environment variable generation
updated: 2026-01-16
---

# Coder-Convex-Setup: Initial Convex Workspace Setup in Coder

You are an expert at **initial setup and configuration** of self-hosted Convex in Coder workspaces. This skill is ONLY for the one-time setup of a new Convex workspace. For everyday Convex development, use the `coder-convex` skill instead.

## When to Use This Skill

Use this skill when:
- Setting up Convex in a new Coder workspace for the first time
- Configuring a self-hosted Convex deployment
- Setting up Docker-based Convex backend
- Configuring environment variables for Convex
- Generating admin keys and deployment URLs

**DO NOT use this skill for:**
- Everyday Convex development (use `coder-convex` instead)
- Writing queries, mutations, or actions (use `coder-convex` instead)
- Schema modifications (use `coder-convex` instead)
- React integration issues (use `coder-convex` instead)

## Prerequisites

Before setting up Convex in a Coder workspace, ensure:

1. **Node.js and a package manager are installed**:
   ```bash
   node --version  # Should be v18+
   # Check for package manager: pnpm, yarn, npm, or bun
   pnpm --version  # Or: yarn --version, npm --version, bun --version
   ```

2. **Docker is available**:
   ```bash
   docker --version
   docker compose version
   ```

3. **Project has package.json with Convex dependency**:
   ```json
   {
     "dependencies": {
       "convex": "^1.31.3"
     }
   }
   ```

## Coder Workspace Services Overview

In a Coder workspace, Convex is exposed through multiple services. Understanding these is critical:

| Slug | Display Name | Internal URL | Port | Hidden | Purpose |
|------|-------------|--------------|------|--------|---------|
| `convex-dashboard` | Convex Dashboard | `localhost:6791` | 6791 | No | Admin dashboard |
| `convex-api` | Convex API | `localhost:3210` | 3210 | **Yes** | Main API endpoints |
| `convex-site` | Convex Site | `localhost:3211` | 3211 | **Yes** | **Site Proxy (Auth)** |

## Step 1: Install Convex Dependencies

```bash
# Install Convex package
[package-manager] add convex

# Install auth dependencies (required for Coder workspaces)
[package-manager] add @convex-dev/auth

# Install dev dependencies if not present
[package-manager] add -D @types/node typescript
```

## Step 2: Create Convex Directory Structure

Create the following directory structure:

```bash
mkdir -p convex/lib
```

The structure should look like:

```
convex/
├── lib/                  # Internal utilities (optional)
├── schema.ts            # Database schema (required)
├── auth.ts              # Auth setup (required for Coder)
├── router.ts            # HTTP routes (required for auth endpoints)
└── http.ts              # HTTP exports with auth routes (required for Coder)
```

## Step 3: Create Initial Schema

Create [convex/schema.ts](convex/schema.ts):

```typescript
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";
import { authTables } from "@convex-dev/auth/server";

// Your application tables
const applicationTables = {
  // Add your tables here
  tasks: defineTable({
    title: v.string(),
    status: v.string(),
  }).index("by_status", ["status"]),
};

export default defineSchema({
  ...authTables,
  ...applicationTables,
});
```

**Key Schema Rules**:
- Always include `...authTables` from `@convex-dev/auth/server` for Coder workspaces
- Never manually add `_id` or `_creationTime` - they're automatic
- Index names should be descriptive: `by_fieldName`
- All indexes automatically include `_creationTime` as the last field
- Don't use `.index("by_creation_time", ["_creationTime"])` - it's built-in

## Step 4: Create Auth Configuration

> **Note**: Modern `@convex-dev/auth` (v0.0.90+) uses the `convexAuth()` function directly. A separate `auth.config.ts` file is no longer required.

Create [convex/auth.ts](convex/auth.ts):

```typescript
import { convexAuth, getAuthUserId } from "@convex-dev/auth/server";
import { Password } from "@convex-dev/auth/providers/Password";
import { Anonymous } from "@convex-dev/auth/providers/Anonymous";
import { query } from "./_generated/server";

// Configure auth with providers
export const { auth, signIn, signOut, store, isAuthenticated } = convexAuth({
  providers: [Password, Anonymous],
});

// Query to get the current user
export const currentUser = query({
  args: {},
  handler: async (ctx) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) {
      return null;
    }
    return await ctx.db.get(userId);
  },
});
```

Create [convex/router.ts](convex/router.ts):

```typescript
import { httpRouter } from "convex/server";

const http = httpRouter();

export default http;
```

Create [convex/http.ts](convex/http.ts):

```typescript
import { auth } from "./auth";
import router from "./router";

const http = router;

// CRITICAL: Add auth routes to the HTTP router
auth.addHttpRoutes(http);

export default http;
```

**Critical**: The `auth.addHttpRoutes(http)` call is required for auth endpoints (`/auth/*`) to be accessible. Without this, authentication will not work.

## Step 5: Create Coder Setup Script

Create [scripts/setup-convex.sh](scripts/setup-convex.sh):

```bash
#!/bin/bash

# Detect Coder workspace environment
# Check for both CODER and CODER_WORKSPACE_NAME to confirm we're in a Coder workspace
if [ -n "$CODER" ] && [ -n "$CODER_WORKSPACE_NAME" ]; then
  # Running in Coder workspace
  # Extract protocol and domain from CODER_URL (e.g., https://coder.hahomelabs.com)
  CODER_PROTOCOL="${CODER_URL%%://*}"
  CODER_DOMAIN="${CODER_URL#*//}"
  WORKSPACE_NAME="${CODER_WORKSPACE_NAME}"
  USERNAME="${CODER_WORKSPACE_OWNER_NAME:-$USER}"

  # Generate Coder-specific URLs
  # Format: <protocol>://<service>--<workspace>--<owner>.<coder-domain>
  CONVEX_API_URL="${CODER_PROTOCOL}://convex-api--${WORKSPACE_NAME}--${USERNAME}.${CODER_DOMAIN}"
  CONVEX_SITE_URL="${CODER_PROTOCOL}://convex-site--${WORKSPACE_NAME}--${USERNAME}.${CODER_DOMAIN}"
  CONVEX_DASHBOARD_URL="${CODER_PROTOCOL}://convex--${WORKSPACE_NAME}--${USERNAME}.${CODER_DOMAIN}"
else
  # Local development
  CONVEX_API_URL="http://localhost:3210"
  CONVEX_SITE_URL="http://localhost:3211"
  CONVEX_DASHBOARD_URL="http://localhost:6791"
fi

# Determine PostgreSQL URL from environment
# Priority order: DATABASE_URL → POSTGRES_URI → POSTGRES_URL
# Note: We strip the database name from the URL since Convex appends INSTANCE_NAME automatically
# E.g., "postgres://...:5432/app" becomes "postgres://...:5432"
_RAW_POSTGRES_URL="${DATABASE_URL:-${POSTGRES_URI:-${POSTGRES_URL:-}}}"
if [ -n "$_RAW_POSTGRES_URL" ]; then
  # Remove trailing database name (e.g., /app) if present
  _STRIPPED_URL="${_RAW_POSTGRES_URL%/[^/]*}"
  # For Coder PostgreSQL with self-signed certificates, use sslmode=disable
  # Note: Rust postgres crate may not accept sslmode parameter in URL, depends on version
  if [[ "$_STRIPPED_URL" == *"?"* ]]; then
    # URL already has query parameters
    POSTGRES_URL="${_STRIPPED_URL}&sslmode=disable"
  else
    # Add query parameters - use disable for self-signed certs
    POSTGRES_URL="${_STRIPPED_URL}?sslmode=disable"
  fi
else
  # Fallback to default for local development
  POSTGRES_URL="postgresql://convex:convex@localhost:5432/convex?sslmode=disable"
fi

# Verify PostgreSQL URL is configured
if [ -z "$POSTGRES_URL" ]; then
  echo "❌ POSTGRES_URL is not set"
  echo "   Please set DATABASE_URL or POSTGRES_URL in your environment"
  echo ""
  echo "   In Coder workspaces, these variables are automatically provided."
  echo "   For local development, ensure PostgreSQL is running and set the variable."
  exit 1
fi

# Admin key will be generated by the container on first start
# The container's generate_admin_key.sh script is the proper way to generate keys
# We'll retrieve it after the container starts
CONVEX_ADMIN_KEY="${CONVEX_ADMIN_KEY:-}"

# Generate JWT private key for auth (PKCS#8 format)
if [ ! -f jwt_private_key.pem ]; then
  openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out jwt_private_key.pem 2>/dev/null
fi

# Create .env.convex.local (only if missing or incomplete)
ENV_FILE=".env.convex.local"
ENV_FILE_MISSING=0

if [ ! -f "$ENV_FILE" ]; then
  echo "📝 Creating $ENV_FILE..."
  ENV_FILE_MISSING=1
else
  # Check if required variables are present
  if ! grep -q "^POSTGRES_URL=" "$ENV_FILE" 2>/dev/null; then
    echo "📝 $ENV_FILE exists but missing POSTGRES_URL, updating..."
    ENV_FILE_MISSING=1
  fi
  if ! grep -q "^CONVEX_CLOUD_ORIGIN=" "$ENV_FILE" 2>/dev/null && [ -n "$CONVEX_API_URL" ]; then
    echo "📝 $ENV_FILE exists but missing Convex URLs, updating..."
    ENV_FILE_MISSING=1
  fi
fi

if [ $ENV_FILE_MISSING -eq 1 ]; then
  # Create or update the env file
  cat > "$ENV_FILE" << ENVEOF
# Self-hosted Convex configuration
# Auto-generated by setup-convex.sh

# PostgreSQL connection URL
POSTGRES_URL=$POSTGRES_URL

# Convex Cloud Origin - External URL for Convex API access
CONVEX_CLOUD_ORIGIN=$CONVEX_CLOUD_ORIGIN

# Convex Site Origin - HTTP actions endpoint (for auth)
CONVEX_SITE_ORIGIN=$CONVEX_SITE_ORIGIN

# Convex Site URL - Used by @convex-dev/auth for provider domain
CONVEX_SITE_URL=$CONVEX_API_URL

# Convex Deployment URL
CONVEX_DEPLOYMENT_URL=$CONVEX_DEPLOYMENT_URL

# Frontend Configuration
VITE_CONVEX_URL=$CONVEX_CLOUD_ORIGIN

# Admin Key will be retrieved from container after it starts
# CONVEX_ADMIN_KEY and CONVEX_SELF_HOSTED_ADMIN_KEY are set by the container

# JWT Configuration (for auth)
# JWT_ISSUER should match CONVEX_SITE_ORIGIN for proper auth validation
JWT_ISSUER=$CONVEX_SITE_ORIGIN
ENVEOF
  echo "✅ Created $ENV_FILE"
fi

# Source environment variables from the (now existing) file
echo "📦 Loading environment variables from $ENV_FILE"
set -a
source "$ENV_FILE"
set +a

echo "Convex environment configured!"
echo "API URL: ${CONVEX_API_URL}"
echo "Site URL: ${CONVEX_SITE_URL}"
echo "Dashboard URL: ${CONVEX_DASHBOARD_URL}"
echo "Admin Key: ${CONVEX_ADMIN_KEY:0:20}..."
```

Make it executable and run:

```bash
chmod +x scripts/setup-convex.sh
./scripts/setup-convex.sh
```

## Step 6: Create Custom Entrypoint Script

Create [convex-backend-entrypoint.sh](convex-backend-entrypoint.sh):

```bash
#!/bin/bash
# Wrapper script to start Convex backend with JWT_PRIVATE_KEY from file
# Based on the original run_backend.sh but with JWT_PRIVATE_KEY loading

set -e

export DATA_DIR=${DATA_DIR:-/convex/data}
export TMPDIR=${TMPDIR:-"$DATA_DIR/tmp"}
export STORAGE_DIR=${STORAGE_DIR:-"$DATA_DIR/storage"}
export SQLITE_DB=${SQLITE_DB:-"$DATA_DIR/db.sqlite3"}

# Database driver flags
POSTGRES_DB_FLAGS=(--db postgres-v5)
MYSQL_DB_FLAGS=(--db mysql-v5)

mkdir -p "$TMPDIR" "$STORAGE_DIR"

# NOTE: INSTANCE_NAME and INSTANCE_SECRET are set via Docker environment variables
# in docker-compose.convex.yml. They are NOT sourced from a credentials script.

# IMPORTANT: Set JWT_PRIVATE_KEY BEFORE sourcing anything else
# This environment variable MUST be set before the Convex backend starts
# for it to be available in the isolate workers
if [ -f /jwt_private_key.pem ]; then
  echo "Loading JWT_PRIVATE_KEY from /jwt_private_key.pem..."
  DECODED_KEY=$(cat /jwt_private_key.pem)
  echo "JWT_PRIVATE_KEY loaded (length: ${#DECODED_KEY})"
  export JWT_PRIVATE_KEY="$DECODED_KEY"
  echo "JWT_PRIVATE_KEY exported successfully"
  echo "Verifying: ${#JWT_PRIVATE_KEY} characters"
elif [ -n "$JWT_PRIVATE_KEY_BASE64" ]; then
  echo "Loading JWT_PRIVATE_KEY from JWT_PRIVATE_KEY_BASE64..."
  DECODED_KEY=$(echo "$JWT_PRIVATE_KEY_BASE64" | base64 -d)
  echo "JWT_PRIVATE_KEY loaded (length: ${#DECODED_KEY})"
  export JWT_PRIVATE_KEY="$DECODED_KEY"
  echo "JWT_PRIVATE_KEY exported successfully"
  echo "Verifying: ${#JWT_PRIVATE_KEY} characters"
fi

# Make JWT_PRIVATE_KEY available to child processes via env file
if [ -n "$JWT_PRIVATE_KEY" ]; then
  # Export to a file that will be sourced by child processes
  # This is necessary because Convex isolate workers don't inherit all environment variables
  echo "export JWT_PRIVATE_KEY=\"$JWT_PRIVATE_KEY\"" > /convex/jwt_env.sh
  echo "JWT environment written to /convex/jwt_env.sh"
  # Source it ourselves for good measure
  . /convex/jwt_env.sh
fi

# Determine database configuration
if [ -n "$POSTGRES_URL" ]; then
  DB_SPEC="$POSTGRES_URL"
  DB_FLAGS=("${POSTGRES_DB_FLAGS[@]}")
elif [ -n "$MYSQL_URL" ]; then
  DB_SPEC="$MYSQL_URL"
  DB_FLAGS=("${MYSQL_DB_FLAGS[@]}")
elif [ -n "$DATABASE_URL" ]; then
  echo "Warning: DATABASE_URL is deprecated."
  DB_SPEC="$DATABASE_URL"
  DB_FLAGS=("${POSTGRES_DB_FLAGS[@]}")
else
  DB_SPEC="$SQLITE_DB"
  DB_FLAGS=()
fi

# Use local storage (S3 not configured)
STORAGE_FLAGS=(--local-storage "$STORAGE_DIR")

# Run the Convex backend with JWT_PRIVATE_KEY explicitly set in the environment
# Using env to ensure the variable is passed to the child process
exec env JWT_PRIVATE_KEY="$JWT_PRIVATE_KEY" "$@" ./convex-local-backend \
  --instance-name "$INSTANCE_NAME" \
  --instance-secret "$INSTANCE_SECRET" \
  --port 3210 \
  --site-proxy-port 3211 \
  --convex-origin "$CONVEX_CLOUD_ORIGIN" \
  --convex-site "$CONVEX_SITE_ORIGIN" \
  --beacon-tag "self-hosted-docker" \
  ${DISABLE_BEACON:+--disable-beacon} \
  ${REDACT_LOGS_TO_CLIENT:+--redact-logs-to-client} \
  ${DO_NOT_REQUIRE_SSL:+--do-not-require-ssl} \
  "${DB_FLAGS[@]}" \
  "${STORAGE_FLAGS[@]}" \
  "$DB_SPEC"
```

Make it executable:
```bash
chmod +x convex-backend-entrypoint.sh
```

## Step 7: Create Docker Compose Configuration

Create [docker-compose.convex.yml](docker-compose.convex.yml):

```yaml
services:
  convex-backend:
    image: ghcr.io/get-convex/convex-backend:latest
    container_name: convex-backend-local
    env_file:
      - .env.convex.local
    stop_grace_period: 10s
    stop_signal: SIGINT
    ports:
      - "3210:3210" # Convex API port
      - "3211:3211" # Convex site proxy port (for auth)
    volumes:
      - convex-data:/convex/data
      - ./convex-backend-entrypoint.sh:/convex-backend-entrypoint.sh:ro
      - ./jwt_private_key.pem:/jwt_private_key.pem:ro
    entrypoint: ["/bin/bash", "/convex-backend-entrypoint.sh"]
    environment:
      # Convex Cloud Origin - External URL for Convex API access
      # For local development, defaults to http://localhost:3210
      # In Coder workspaces, set via .env.convex.local
      - CONVEX_CLOUD_ORIGIN=${CONVEX_CLOUD_ORIGIN:-http://localhost:3210}
      # Convex Site Origin - HTTP actions endpoint (for auth)
      # For local development, defaults to http://localhost:3211
      # In Coder workspaces, set via .env.convex.local
      - CONVEX_SITE_ORIGIN=${CONVEX_SITE_ORIGIN:-http://localhost:3211}
      # PostgreSQL Database URL (required)
      - POSTGRES_URL=${POSTGRES_URL}
      # Instance name for identification (matches PostgreSQL database name)
      - INSTANCE_NAME=app
      # Admin key for authentication (generated on first start)
      - CONVEX_ADMIN_KEY=${CONVEX_ADMIN_KEY:-}
      # Logging
      - RUST_LOG=info,convex=debug
      # Lower document retention for development
      - DOCUMENT_RETENTION_DELAY=172800
      # Disable SSL requirement for local development
      - DO_NOT_REQUIRE_SSL=true
      # Auth configuration for @convex-dev/auth
      # Note: JWT_PRIVATE_KEY is set by convex-backend-entrypoint.sh from mounted file
      - JWT_ISSUER=${JWT_ISSUER:-http://localhost:3211}
      # Instance secret (auto-generated by backend if not set)
      - INSTANCE_SECRET=${INSTANCE_SECRET:-}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3210/version"]
      interval: 5s
      start_period: 10s
      timeout: 5s
      retries: 3

  convex-dashboard:
    image: ghcr.io/get-convex/convex-dashboard:latest
    container_name: convex-dashboard-local
    env_file:
      - .env.convex.local
    stop_grace_period: 10s
    stop_signal: SIGINT
    ports:
      - "6791:6791" # Dashboard port
    environment:
      # Deployment URL for dashboard
      - NEXT_PUBLIC_DEPLOYMENT_URL=${CONVEX_DEPLOYMENT_URL:-http://localhost:3210}
    depends_on:
      convex-backend:
        condition: service_healthy

volumes:
  convex-data:
    driver: local
```

**Critical Configuration Explained:**
- **Custom Entrypoint**: Loads `JWT_PRIVATE_KEY` from mounted file before starting backend
- **Volume Mount**: `jwt_private_key.pem` is mounted at `/jwt_private_key.pem:ro`
- **Ports**: 3210 (API), 3211 (site proxy for auth), 6791 (dashboard)
- **`CONVEX_CLOUD_ORIGIN`**: External URL for the API (for internal Convex communication)
- **`CONVEX_SITE_ORIGIN`**: External URL for the site proxy (for auth provider discovery, set via `npx convex env set`)
- **`JWT_ISSUER`**: Points to site proxy URL
- **Healthcheck**: Ensures backend is ready before dashboard starts

## Step 8: Create Startup Script

Create [start-convex-backend.sh](start-convex-backend.sh):

```bash
#!/bin/bash

# Load environment
if [ -f .env.convex.local ]; then
  set -a
  source .env.convex.local
  set +a
fi

# Start Docker services
docker compose -f docker-compose.convex.yml up -d

echo "Waiting for Convex backend to be healthy..."
until curl -s http://localhost:3210/version > /dev/null 2>&1; do
  echo "Waiting for Convex API..."
  sleep 2
done

echo "Convex backend is running!"
echo "Dashboard: ${CONVEX_DASHBOARD_URL:-http://localhost:6791}"
```

> **CRITICAL DEPLOYMENT ORDER**: The startup sequence must follow this order:
> 1. Start Docker services (backend becomes healthy)
> 2. **Initialize deployment environment variables** (`npx convex env set`) - These MUST be set before deployment!
> 3. **Then deploy functions** (`npx convex deploy --yes`)
>
> Why this order: Auth-related environment variables (like `CONVEX_SITE_ORIGIN`, `JWT_ISSUER`, `JWKS`) must be set **before** deploying functions. If you deploy first, the deployment may fail or auth may not work properly.

## Step 9: Add NPM Scripts

Add these scripts to your [package.json](package.json):

```json
{
  "scripts": {
    "dev": "npm-run-all --parallel dev:frontend convex:start",
    "dev:frontend": "vite",
    "dev:backend": "convex dev --local --once",
    "convex:start": "./scripts/setup-convex.sh",
    "convex:stop": "docker compose -f docker-compose.convex.yml down",
    "convex:logs": "docker compose -f docker-compose.convex.yml logs -f",
    "convex:status": "docker compose -f docker-compose.convex.yml ps",
    "deploy:functions": "npx convex deploy --yes"
  }
}
```

**Script explanations:**
- `dev` - Starts both frontend and Convex backend in parallel
- `dev:frontend` - Runs the frontend development server (Vite, Next.js, etc.)
- `dev:backend` - Runs Convex in development mode against local backend, then exits
- `convex:start` - Sets up environment and starts Docker services
- `convex:stop` - Stops Docker services
- `convex:logs` - Shows Convex backend logs
- `convex:status` - Shows status of Docker containers
- `deploy:functions` - Deploys Convex functions to the self-hosted backend

## Step 10: Initialize Convex Deployment

```bash
# Setup environment and start backend
[package-manager] run convex:start

# Initialize Convex (creates schema, generates types)
[package-manager] run dev:backend
```

This will:
1. Generate Coder-specific environment variables
2. Start Docker services with correct configuration
3. Create the database schema
4. Generate type definitions in `convex/_generated/`

## Step 11: Initialize Deployment Environment Variables

**IMPORTANT**: Run this step BEFORE deploying functions. Auth environment variables must be set first.

Create [scripts/init-convex-env.sh](scripts/init-convex-env.sh):

```bash
#!/bin/bash
# Initialize Convex deployment environment variables
# Reads from .env.convex.deployment and sets variables via npx convex env set

set -e

DEPLOYMENT_ENV_FILE=".env.convex.deployment"
CONTAINER_ENV_FILE=".env.convex.local"

echo "🔐 Initializing Convex deployment environment variables..."

# Create deployment env file if it doesn't exist
if [ ! -f "$DEPLOYMENT_ENV_FILE" ]; then
    echo "📝 Creating $DEPLOYMENT_ENV_FILE..."
    cat > "$DEPLOYMENT_ENV_FILE" << 'EOF'
# Convex Deployment Environment Variables
# These variables are set via npx convex env set and appear in the dashboard
# This file should be gitignored (contains secrets)

# === AUTO-GENERATED VARIABLES (do not edit manually) ===
# These are managed by scripts/init-convex-env.sh
# Multi-line values are stored as base64 for safe env file storage
JWT_PRIVATE_KEY_BASE64=""
JWT_ISSUER=""
JWKS=""

# === USER VARIABLES (add your own below) ===
# Add your environment variables here, one per line
# Example:
# OPENAI_API_KEY=sk-...
# STRIPE_SECRET_KEY=sk_live_...
# ANTHROPIC_API_KEY=sk-ant-...
EOF
fi

# Source container env file to get CONVEX_SITE_ORIGIN
set -a
source "$CONTAINER_ENV_FILE"
set +a

# Check if JWT key file exists and has content
JWT_KEY_FILE="jwt_private_key.pem"

if [ -f "$JWT_KEY_FILE" ] && [ -s "$JWT_KEY_FILE" ]; then
    # Read existing key from file
    JWT_PRIVATE_KEY=$(cat "$JWT_KEY_FILE")
    echo "📂 Using existing JWT key from $JWT_KEY_FILE"
else
    # Generate a new key
    echo "🔑 Generating new JWT private key..."
    JWT_PRIVATE_KEY=$(openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 2>/dev/null | openssl pkcs8 -topk8 -nocrypt -outform PEM 2>/dev/null)

    if [ -z "$JWT_PRIVATE_KEY" ]; then
        echo "❌ Failed to generate JWT private key"
        exit 1
    fi

    echo "✅ Generated new JWT private key"

    # Write the key to the host file for persistence
    echo "$JWT_PRIVATE_KEY" > "$JWT_KEY_FILE"
    echo "📝 Saved key to $JWT_KEY_FILE"
    echo ""
    echo "⚠️  Note: The convex-backend container will use this key on next restart."
    echo "   To restart: docker compose -f docker-compose.convex.yml restart convex-backend"
fi

# Generate JWKS from private key
echo "🔑 Generating JWKS from private key..."
JWKS=$(node -e "
const crypto = require('crypto');
const privateKey = \`$JWT_PRIVATE_KEY\`;
const publicKey = crypto.createPublicKey(privateKey);
const jwk = publicKey.export({ format: 'jwk' });
// JWKS format requires {\"keys\": [...]} wrapper
const jwks = { keys: [{ use: 'sig', ...jwk }] };
console.log(JSON.stringify(jwks));
")

# Update auto-generated variables in the deployment env file
echo "📝 Updating auto-generated variables in $DEPLOYMENT_ENV_FILE..."
TEMP_FILE=$(mktemp)

# Encode the multi-line JWT private key as base64 for safe env file storage
JWT_PRIVATE_KEY_BASE64=$(echo "$JWT_PRIVATE_KEY" | base64 -w 0)

# Process the file and update auto-generated variables
while IFS= read -r line || [ -n "$line" ]; do
    if [[ "$line" =~ ^JWT_PRIVATE_KEY_BASE64= ]]; then
        echo "JWT_PRIVATE_KEY_BASE64=\"$JWT_PRIVATE_KEY_BASE64\""
    elif [[ "$line" =~ ^JWT_ISSUER= ]]; then
        echo "JWT_ISSUER=\"$CONVEX_SITE_ORIGIN\""
    elif [[ "$line" =~ ^JWKS= ]]; then
        echo "JWKS=\"$JWKS\""
    else
        echo "$line"
    fi
done < "$DEPLOYMENT_ENV_FILE" > "$TEMP_FILE"

mv "$TEMP_FILE" "$DEPLOYMENT_ENV_FILE"

# Now set all variables via npx convex env set
echo "📤 Setting deployment environment variables..."

# Set JWT_PRIVATE_KEY (multi-line value, use stdin)
echo "  Setting JWT_PRIVATE_KEY..."
if ! echo "$JWT_PRIVATE_KEY" | npx convex env set JWT_PRIVATE_KEY; then
    echo "❌ Failed to set JWT_PRIVATE_KEY"
    exit 1
fi

# Set CONVEX_SITE_ORIGIN (required for auth provider discovery)
echo "  Setting CONVEX_SITE_ORIGIN..."
if ! npx convex env set CONVEX_SITE_ORIGIN "$CONVEX_SITE_ORIGIN"; then
    echo "❌ Failed to set CONVEX_SITE_ORIGIN"
    exit 1
fi

# Set JWT_ISSUER
echo "  Setting JWT_ISSUER..."
if ! npx convex env set JWT_ISSUER "$CONVEX_SITE_ORIGIN"; then
    echo "❌ Failed to set JWT_ISSUER"
    exit 1
fi

# Set JWKS (multi-line value, use stdin)
echo "  Setting JWKS..."
if ! echo "$JWKS" | npx convex env set JWKS; then
    echo "❌ Failed to set JWKS"
    exit 1
fi

# Now set user variables from the deployment env file
# Parse only the user section (after the USER VARIABLES comment)
USER_SECTION=false
while IFS= read -r line || [ -n "$line" ]; do
    # Start processing after USER VARIABLES comment
    if [[ "$line" == *"USER VARIABLES"* ]]; then
        USER_SECTION=true
        continue
    fi

    # Only process user variables
    [ "$USER_SECTION" = false ] && continue

    # Skip comments and empty lines
    [[ "$line" == \#* ]] && continue
    [ -z "$line" ] && continue

    # Extract variable name and value
    VAR_NAME="${line%%=*}"
    VAR_VALUE="${line#*=}"

    # Skip empty values
    [ -z "$VAR_VALUE" ] && continue

    echo "  Setting $VAR_NAME..."
    npx convex env set "$VAR_NAME" "$VAR_VALUE"
done < "$DEPLOYMENT_ENV_FILE"

echo "✅ Convex deployment environment variables initialized"
echo "   Verify in dashboard: Environment Variables section"
```

Make it executable:
```bash
chmod +x scripts/init-convex-env.sh
```

Run the script to initialize deployment environment variables:
```bash
bash scripts/init-convex-env.sh
```

**What this script does:**
1. Creates `.env.convex.deployment` file for tracking deployment variables
2. Generates or reads existing JWT private key from `jwt_private_key.pem`
3. Generates JWKS from the private key using Node.js crypto API
4. Sets `JWT_PRIVATE_KEY`, `CONVEX_SITE_ORIGIN`, `JWT_ISSUER`, and `JWKS` via `npx convex env set`
5. Sets any user-defined variables from the deployment env file

> **Note**: The `.env.convex.deployment` file uses `JWT_PRIVATE_KEY_BASE64` for safe storage of the multi-line key as a single-line value. The script decodes it before setting in Convex.

## Step 12: Deploy Functions

Now that environment variables are initialized, deploy your Convex functions:

```bash
[package-manager] run deploy:functions
```

This deploys your Convex functions to the self-hosted backend.

> **Why this order matters**: Auth-related environment variables (`CONVEX_SITE_ORIGIN`, `JWT_ISSUER`, `JWKS`) must be set **before** deploying functions. If you deploy first, the deployment may fail or authentication may not work properly.

## Step 13: Create Frontend Integration

Create or update [src/main.tsx](src/main.tsx):

```typescript
import { ConvexReactClient } from "convex/react";
import { ConvexProviderWithAuth } from "convex/react";
import React from "react";
import ReactDOM from "react-dom/client";

const convex = new ConvexReactClient(import.meta.env.VITE_CONVEX_URL);

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <ConvexProviderWithAuth client={convex}>
      <App />
    </ConvexProviderWithAuth>
  </React.StrictMode>
);
```

Create [src/App.tsx](src/App.tsx):

```typescript
import { useQuery } from "convex/react";
import { api } from "../convex/_generated/api";
import { SignInButton, SignOutButton, useAuth } from "@convex-dev/auth/react";

export default function App() {
  const { isAuthenticated } = useAuth();
  const tasks = useQuery(api.tasks.list) || [];

  return (
    <main>
      <h1>Convex in Coder</h1>
      {isAuthenticated ? (
        <>
          <p>Welcome!</p>
          <SignOutButton />
          <ul>
            {tasks.map(task => (
              <li key={task._id}>{task.title}</li>
            ))}
          </ul>
        </>
      ) : (
        <SignInButton />
      )}
    </main>
  );
}
```

## Verification Checklist

After setup, verify:

- [ ] `.env.convex.local` exists with correct Coder URLs
- [ ] `convex/_generated/` directory exists with type definitions
- [ ] `convex/schema.ts` includes `...authTables`
- [ ] `convex/auth.ts` uses `convexAuth()` with providers
- [ ] `convex/http.ts` calls `auth.addHttpRoutes(http)`
- [ ] Docker services are running: `docker ps`
- [ ] Can access API: `curl http://localhost:3210/version`
- [ ] Can access site proxy: `curl http://localhost:3211/`
- [ ] Can run `[package-manager] run dev:backend` without errors
- [ ] Can run `[package-manager] run deploy:functions` successfully
- [ ] Frontend can import from `convex/_generated/api`

## Troubleshooting Setup Issues

### Issue: Authentication fails

**Solution**: Verify your environment variables:
```bash
grep "CONVEX_SITE" .env.convex.local
# CONVEX_SITE_ORIGIN should point to convex-site URL (port 3211)
# JWT_ISSUER should match CONVEX_SITE_ORIGIN
```

### Issue: `CONVEX_SITE_ORIGIN not set in deployment`

**Solution**: Run `./scripts/setup-convex.sh` to regenerate environment.

### Issue: Port 3211 not accessible

**Solution**: Verify Docker is running the site proxy:
```bash
docker ps | grep 3211
curl http://localhost:3211/
```

### Issue: Docker container not starting

**Solution**:
```bash
# Check container logs
[package-manager] run convex:logs

# Check if ports are already in use
lsof -i :3210
lsof -i :3211
lsof -i :6791

# Recreate container
[package-manager] run convex:stop
[package-manager] run convex:start
```

### Issue: Type definitions not generating

**Solution**:
```bash
# Clear Convex cache
rm -rf convex/_generated

# Re-run dev backend
[package-manager] run dev:backend

# Or explicitly deploy
[package-manager] run deploy:functions
```

### Issue: Cannot connect to Convex deployment

**Solution**:
```bash
# Verify Docker services are running
docker ps

# Check deployment URL is correct
grep CONVEX .env.convex.local

# Test connection
curl $CONVEX_CLOUD_ORIGIN/version
curl $CONVEX_SITE_ORIGIN/
```

## Coder Workspace URL Patterns

### Internal (Localhost)

| Service | URL |
|---------|-----|
| Convex API | `http://localhost:3210` |
| Site Proxy (Auth) | `http://localhost:3211` |
| Dashboard | `http://localhost:6791` |

### External (Coder Proxy)

| Service | URL Pattern | Example |
|---------|-------------|---------|
| Convex API | `https://convex-api--<workspace>--<user>.<domain>` | `https://convex-api--myproject--johndoe.coder.hahomelabs.com` |
| Convex Site | `https://convex-site--<workspace>--<user>.<domain>` | `https://convex-site--myproject--johndoe.coder.hahomelabs.com` |
| Convex Dashboard | `https://convex--<workspace>--<user>.<domain>` | `https://convex--myproject--johndoe.coder.hahomelabs.com` |

## Environment Variables Reference

### Required for Coder Convex

```bash
# Coder Workspace URLs (auto-generated by setup script)
CONVEX_CLOUD_ORIGIN=<convex-api URL>       # e.g., https://convex-api--...coder.hahomelabs.com
CONVEX_SITE_ORIGIN=<convex-site URL>       # e.g., https://convex-site--...coder.hahomelabs.com
CONVEX_DEPLOYMENT_URL=<convex-api URL>     # Same as CONVEX_CLOUD_ORIGIN

# Frontend Configuration
VITE_CONVEX_URL=<convex-api URL>           # Same as CONVEX_CLOUD_ORIGIN

# Admin Key
CONVEX_SELF_HOSTED_ADMIN_KEY=<admin-key>   # Auto-generated

# JWT Configuration (for auth)
JWT_ISSUER=<convex-site URL>               # Same as CONVEX_SITE_ORIGIN
# JWT_PRIVATE_KEY is loaded from jwt_private_key.pem via entrypoint script

# Database (if using PostgreSQL)
POSTGRES_URL=<postgres-connection-string>  # e.g., postgresql://convex:convex@localhost:5432/convex
```

### Critical Variable Relationships

```
CONVEX_CLOUD_ORIGIN = CONVEX_DEPLOYMENT_URL = VITE_CONVEX_URL (all point to convex-api, port 3210)
CONVEX_SITE_ORIGIN = JWT_ISSUER (both point to convex-site, port 3211)
```

**Why this works:**
- All Convex client communication goes through the API (port 3210)
- The `CONVEX_SITE_ORIGIN` is used for auth provider discovery (set via `npx convex env set`)
- The site proxy (port 3211) handles HTTP routes and auth endpoint discovery
- JWT tokens are validated against the `JWT_ISSUER` which must match `CONVEX_SITE_ORIGIN`

## Docker Commands Reference

```bash
# Start services
[package-manager] run convex:start                    # Setup and start all services

# Stop services
[package-manager] run convex:stop                     # Stop all services

# View logs
[package-manager] run convex:logs                     # View backend logs

# Check status
[package-manager] run convex:status                   # Check container status

# Restart services
docker compose -f docker-compose.convex.yml restart

# Execute command in container
docker exec -it <container-name> sh
```

## Post-Setup: Next Steps

After completing the setup:

1. **Switch to `coder-convex` skill** for everyday development
2. **Define your schema** in `convex/schema.ts` (in `applicationTables`)
3. **Write queries and mutations** in `convex/*.ts` files
4. **Integrate with React** using `convex/react` hooks
5. **Deploy functions** with `[package-manager] run deploy:functions]`

## Common Setup Patterns

### Pattern 1: Minimal Setup with Auth

```typescript
// convex/schema.ts
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";
import { authTables } from "@convex-dev/auth/server";

const applicationTables = {
  tasks: defineTable({
    title: v.string(),
    status: v.string(),
    userId: v.id("users"),
  }).index("by_user", ["userId"]),
};

export default defineSchema({
  ...authTables,
  ...applicationTables,
});
```

### Pattern 2: With AI/RAG

Requires:
- `OPENAI_API_KEY` in environment
- `ENABLE_RAG=true`
- Embeddings generation script

## Quick Setup Command Sequence

For a complete fresh setup:

```bash
# 1. Install dependencies
[package-manager] add convex @convex-dev/auth
[package-manager] add -D @types/node typescript

# 2. Create directories
mkdir -p convex lib scripts

# 3. Create schema with auth
cat > convex/schema.ts << 'EOF'
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";
import { authTables } from "@convex-dev/auth/server";

const applicationTables = {
  tasks: defineTable({
    title: v.string(),
    status: v.string(),
  }).index("by_status", ["status"]),
};

export default defineSchema({
  ...authTables,
  ...applicationTables,
});
EOF

# 4. Create auth file
cat > convex/auth.ts << 'EOF'
import { convexAuth, getAuthUserId } from "@convex-dev/auth/server";
import { Password } from "@convex-dev/auth/providers/Password";
import { Anonymous } from "@convex-dev/auth/providers/Anonymous";
import { query } from "./_generated/server";

export const { auth, signIn, signOut, store, isAuthenticated } = convexAuth({
  providers: [Password, Anonymous],
});

export const currentUser = query({
  args: {},
  handler: async (ctx) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) return null;
    return await ctx.db.get(userId);
  },
});
EOF

# 5. Create HTTP router files
cat > convex/router.ts << 'EOF'
import { httpRouter } from "convex/server";
const http = httpRouter();
export default http;
EOF

cat > convex/http.ts << 'EOF'
import { auth } from "./auth";
import router from "./router";
const http = router;
auth.addHttpRoutes(http);
export default http;
EOF

# 6. Create setup script (copy from Step 5 above)
# ...

# 7. Create docker-compose file (copy from Step 7 above)
# ...

# 8. Run setup
[package-manager] run convex:start

# 9. Initialize env vars and deploy
bash scripts/init-convex-env.sh
[package-manager] run deploy:functions
```

## Summary

This skill covers the **one-time setup** of self-hosted Convex in Coder workspaces:

1. Install dependencies (including `@convex-dev/auth`)
2. Create directory structure
3. Define schema with auth tables
4. Configure auth (`convexAuth()` in `auth.ts`, `router.ts`, `http.ts`)
5. Create Coder-specific setup script
6. Configure Docker with proper flags
7. Generate environment variables
8. Initialize deployment environment variables
9. Deploy functions
10. Verify setup

For **everyday Convex development** (queries, mutations, React integration, etc.), use the `coder-convex` skill instead.

## Working Example Reference

For a complete, working implementation of self-hosted Convex in a Coder workspace, you can reference:

**[jovermier/convex-ai-chat](https://github.com/jovermier/convex-ai-chat)**

This project demonstrates:
- Self-hosted Convex deployment with Docker Compose
- Complete authentication setup using `@convex-dev/auth`
- Coder workspace environment configuration
- PostgreSQL database integration
- React frontend with Convex integration
- **`start.sh` and `stop.sh` scripts** that fully sequence the initialization (env files, admin key generation, deployment)

**Use this reference to:**
- See how all the pieces connect in a real project
- Verify your setup against a working implementation
- Copy configuration patterns (docker-compose, environment setup, scripts)
- Reference the `start.sh` script for the complete initialization sequence

**Note:** This is a demonstration project. Follow the setup steps in this skill for your own project rather than cloning the repo directly.

## Key Differences from Standard Convex

| Aspect | Standard Convex | Coder Convex |
|--------|----------------|--------------|
| **Deployment URL** | `*.convex.cloud` | Custom Coder proxy URL |
| **Environment Variables** | `CONVEX_DEPLOYMENT` | `CONVEX_CLOUD_ORIGIN`, `CONVEX_SITE_ORIGIN` |
| **Auth Configuration** | Uses Convex Cloud | Uses `convexAuth()` with providers, `CONVEX_SITE_ORIGIN` (site proxy, port 3211) |
| **Site Proxy Port** | Not applicable | 3211 |
| **Dashboard** | Web dashboard at convex.dev | Local at `localhost:6791` |
| **Setup Script** | Guided in dashboard | Custom `setup-convex.sh` script |
