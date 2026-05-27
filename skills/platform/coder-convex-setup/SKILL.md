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
├── auth.config.ts       # Auth configuration (required for Coder)
└── auth.ts              # Auth setup (required for Coder)
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

Create [convex/auth.config.ts](convex/auth.config.ts):

```typescript
export default {
  providers: [
    {
      domain: process.env.CONVEX_SITE_URL,
      applicationID: "convex",
    },
  ],
};
```

**Critical:** The `domain` must use `CONVEX_SITE_URL` which points to the **API URL** (port 3210), not the site proxy URL. Auth endpoints are served at `/api/auth/*` on the API.

Create [convex/auth.ts](convex/auth.ts):

```typescript
import { query } from "./_generated/server";
import { getAuthUserId } from "@convex-dev/auth/server";

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

## Step 5: Create Coder Setup Script

Create [scripts/setup-convex.sh](scripts/setup-convex.sh):

```bash
#!/bin/bash

# Detect Coder workspace environment
if [ -n "$CODER_WORKSPACE_NAME" ]; then
  # Running in Coder workspace
  WORKSPACE_NAME="${CODER_WORKSPACE_NAME}"
  USERNAME="${CODER_USERNAME}"
  CODER_DOMAIN="${CODER_DOMAIN:-coder.hahomelabs.com}"
  CODER_PROTOCOL="${CODER_PROTOCOL:-https}"

  # Generate Coder-specific URLs
  CONVEX_API_URL="${CODER_PROTOCOL}://convex-api--${WORKSPACE_NAME}--${USERNAME}.${CODER_DOMAIN}"
  CONVEX_SITE_URL="${CODER_PROTOCOL}://convex-site--${WORKSPACE_NAME}--${USERNAME}.${CODER_DOMAIN}"
  CONVEX_DASHBOARD_URL="${CODER_PROTOCOL}://convex--${WORKSPACE_NAME}--${USERNAME}.${CODER_DOMAIN}"
else
  # Local development
  CONVEX_API_URL="http://localhost:3210"
  CONVEX_SITE_URL="http://localhost:3211"
  CONVEX_DASHBOARD_URL="http://localhost:6791"
fi

# Generate admin key
CONVEX_ADMIN_KEY="${CONVEX_ADMIN_KEY:-sk_admin_$(openssl rand -hex 32)}"

# Generate JWT private key for auth
if [ ! -f .jwt_private_key ]; then
  openssl genrsa -out .jwt_private_key 2048 2>/dev/null
fi
JWT_PRIVATE_KEY_BASE64=$(base64 -w 0 .jwt_private_key 2>/dev/null || echo "")

# Create .env.convex.local
cat > .env.convex.local << ENVEOF
# Coder Workspace URLs (for remote users)
CONVEX_CLOUD_ORIGIN=${CONVEX_API_URL}
CONVEX_SITE_ORIGIN=${CONVEX_SITE_URL}
CONVEX_SITE_URL=${CONVEX_API_URL}
CONVEX_DEPLOYMENT_URL=${CONVEX_API_URL}

# Frontend Configuration
VITE_CONVEX_URL=${CONVEX_API_URL}

# Admin Key
CONVEX_SELF_HOSTED_ADMIN_KEY=${CONVEX_ADMIN_KEY}

# JWT Configuration (for auth)
JWT_ISSUER=${CONVEX_SITE_URL}
JWT_PRIVATE_KEY_BASE64=${JWT_PRIVATE_KEY_BASE64}

# Database (if using PostgreSQL)
POSTGRES_URL=${POSTGRES_URL:-postgresql://convex:convex@localhost:5432/convex?sslmode=disable}
ENVEOF

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

## Step 6: Create Docker Compose Configuration

Create [docker-compose.convex.yml](docker-compose.convex.yml):

```yaml
services:
  backend:
    image: convex-dev/convex:latest
    ports:
      - "3210:3210"  # API port
      - "3211:3211"  # Site proxy port (auth)
      - "6791:6791"  # Dashboard port
    environment:
      - CONVEX_LOG_LEVEL=info
      - CONVEX_CLOUD_ORIGIN=${CONVEX_CLOUD_ORIGIN}
      - CONVEX_SITE_ORIGIN=${CONVEX_SITE_ORIGIN}
      - CONVEX_SITE_URL=${CONVEX_SITE_URL}
      - CONVEX_DEPLOYMENT_URL=${CONVEX_DEPLOYMENT_URL}
      - JWT_ISSUER=${JWT_ISSUER}
      - JWT_PRIVATE_KEY_BASE64=${JWT_PRIVATE_KEY_BASE64}
      - POSTGRES_URL=${POSTGRES_URL}
    volumes:
      - convex_data:/convex/data
      - ./.jwt_private_key:/convex/jwt_private_key:ro
    restart: unless-stopped
    command: >
      convex backend
      --port 3210
      --site-proxy-port 3211
      --convex-origin "$CONVEX_CLOUD_ORIGIN"
      --convex-site "$CONVEX_SITE_ORIGIN"
      --udf-serving-url "$CONVEX_SITE_URL"

  postgres:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=convex
      - POSTGRES_PASSWORD=convex
      - POSTGRES_DB=convex
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped
    ports:
      - "5432:5432"

volumes:
  convex_data:
  postgres_data:
```

**Critical Flags Explained:**
- `--port 3210`: API port for all Convex communication
- `--site-proxy-port 3211`: Site proxy port for HTTP routes and auth
- `--convex-origin`: External URL for the API (for internal Convex communication)
- `--convex-site`: External URL for the site proxy (for auth provider discovery)

## Step 7: Create Startup Script

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

## Step 8: Add NPM Scripts

Add these scripts to your [package.json](package.json):

```json
{
  "scripts": {
    "convex:start": "./scripts/setup-convex.sh && ./start-convex-backend.sh",
    "convex:stop": "docker compose -f docker-compose.convex.yml down",
    "convex:logs": "docker compose -f docker-compose.convex.yml logs -f backend",
    "convex:status": "docker compose -f docker-compose.convex.yml ps",
    "dev:backend": "npx convex dev --cmd 'node -e \"process.exit(0)\"'",
    "deploy:functions": "npx convex deploy --yes"
  }
}
```

## Step 9: Initialize Convex Deployment

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

## Step 10: Deploy Functions

```bash
[package-manager] run deploy:functions
```

This deploys your Convex functions to the self-hosted backend.

## Step 11: Create Frontend Integration

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
- [ ] `convex/auth.config.ts` uses `CONVEX_SITE_URL` for domain
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
# CONVEX_SITE_ORIGIN should point to convex-site URL
# CONVEX_SITE_URL should point to convex-api URL
```

### Issue: `CONVEX_SITE_URL not set`

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
CONVEX_SITE_URL=<convex-api URL>           # Same as CONVEX_CLOUD_ORIGIN (used by auth.config.ts)
CONVEX_DEPLOYMENT_URL=<convex-api URL>     # Same as CONVEX_CLOUD_ORIGIN

# Frontend Configuration
VITE_CONVEX_URL=<convex-api URL>           # Same as CONVEX_CLOUD_ORIGIN

# Admin Key
CONVEX_SELF_HOSTED_ADMIN_KEY=<admin-key>   # Auto-generated

# JWT Configuration (for auth)
JWT_ISSUER=<convex-site URL>               # Same as CONVEX_SITE_ORIGIN
JWT_PRIVATE_KEY_BASE64=<base64-key>        # Auto-generated

# Database (if using PostgreSQL)
POSTGRES_URL=<postgres-connection-string>  # e.g., postgresql://convex:convex@localhost:5432/convex
```

### Critical Variable Relationships

```
CONVEX_CLOUD_ORIGIN = CONVEX_SITE_URL = CONVEX_DEPLOYMENT_URL = VITE_CONVEX_URL (all point to convex-api)
CONVEX_SITE_ORIGIN = JWT_ISSUER (both point to convex-site)
```

**Why this works:**
- All Convex client communication goes through the API (port 3210)
- Auth endpoints are `/api/auth/*` on the API
- The site proxy (port 3211) is for HTTP routes and internal Convex communication
- The `domain` in `auth.config.ts` uses `CONVEX_SITE_URL` (API URL) because auth endpoints are on the API

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

# 3. Create auth config
cat > convex/auth.config.ts << 'EOF'
export default {
  providers: [
    {
      domain: process.env.CONVEX_SITE_URL,
      applicationID: "convex",
    },
  ],
};
EOF

# 4. Create schema with auth
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

# 5. Create setup script (copy from Step 5 above)
# ...

# 6. Create docker-compose file (copy from Step 6 above)
# ...

# 7. Run setup
[package-manager] run convex:start

# 8. Initialize and deploy
[package-manager] run dev:backend
[package-manager] run deploy:functions
```

## Summary

This skill covers the **one-time setup** of self-hosted Convex in Coder workspaces:

1. Install dependencies (including `@convex-dev/auth`)
2. Create directory structure
3. Define schema with auth tables
4. Configure auth (`auth.config.ts` and `auth.ts`)
5. Create Coder-specific setup script
6. Configure Docker with proper flags
7. Generate environment variables
8. Initialize deployment
9. Verify setup

For **everyday Convex development** (queries, mutations, React integration, etc.), use the `coder-convex` skill instead.

## Key Differences from Standard Convex

| Aspect | Standard Convex | Coder Convex |
|--------|----------------|--------------|
| **Deployment URL** | `*.convex.cloud` | Custom Coder proxy URL |
| **Environment Variables** | `CONVEX_DEPLOYMENT` | `CONVEX_CLOUD_ORIGIN`, `CONVEX_SITE_ORIGIN`, `CONVEX_SITE_URL` |
| **Auth Configuration** | Uses Convex Cloud | Points to `CONVEX_SITE_URL` (API URL) |
| **Site Proxy Port** | Not applicable | 3211 |
| **Dashboard** | Web dashboard at convex.dev | Local at `localhost:6791` |
| **Setup Script** | Guided in dashboard | Custom `setup-convex.sh` script |
