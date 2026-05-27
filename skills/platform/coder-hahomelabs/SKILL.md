---
name: coder-hahomelabs
description: Coder workspace environment for hahomelabs.com deployments. Includes networking, ports, convex config, nhost config
---

# Coder Workspace Environment (hahomelabs.com)

Context for projects running in this Coder workspace environment at hahomelabs.com.

## Environment

You are running in a **Coder development workspace**:

| Property | Value |
|----------|-------|
| **OS** | Linux (Ubuntu/Debian-based) |
| **Architecture** | x86_64 |
| **Container Runtime** | Docker-in-Docker capability via envbox |
| **Infrastructure** | Kubernetes-managed workspace with persistent storage |
| **Networking** | Internal cluster networking with port forwarding capabilities |
| **Shell** | Bash |
| **System Package Manager** | `apt`/`apt-get` |

## Available Tools

The following tools are pre-installed and available in this workspace:

| Tool | Command | Description |
|------|---------|-------------|
| **Docker** | `docker`, `docker-compose` | Full container management capability |
| **Kubernetes CLI** | `kubectl` | Cluster access and management (requires VPN) |
| **GitHub CLI** | `gh` | Pre-configured with auto OAuth token refresh |
| **VS Code Server** | IDE with extensions |
| **Coder CLI** | `coder` | Coder-specific workspace operations |
| **PM2** | `pm2` | Process manager for keeping Node.js services running in the background |
| **Node.js (with pnpm)** | `node`, `pnpm` | Node.js runtime and pnpm package manager |
| **Convex CLI** | `npx convex` | Available when Convex feature is enabled |
| **Claude Code** | `claude` | AI-powered CLI (custom installation via base image) |
| **ccusage** | `ccusage` | Claude Code usage monitoring utility |
| **OpenCode** | `opencode` | AI CLI tool |

## Service URLs

Services use this URL pattern:

```
https://<service>--<workspace-name>--<username>.coder.hahomelabs.com
```

| Service | Port | URL Example |
|---------|------|-------------|
| Dev server | 3000 | `https://app--myproject--johndoe.coder.hahomelabs.com` |
| Prod/preview | 3010 | `https://app-prod--myproject--johndoe.coder.hahomelabs.com` |

**IMPORTANT**: Always use full URLs. Do NOT use `localhost:` URLs as they cause issues with remote services, authentication, cookies, and cross-origin requests.

## Optional Features (Enabled at Workspace Creation)

### PostgreSQL (CloudNativePG)

When enabled, these environment variables are available:

```bash
POSTGRES_HOST     # <workspace-full-name>-db-rw
POSTGRES_PORT     # 5432
POSTGRES_DATABASE # app
POSTGRES_USER     # app
POSTGRES_PASSWORD # Auto-generated
DATABASE_URL      # postgres://app:password@host:port/app
DIRECT_URL        # postgres://app:password@host:port/app
```

**Database details**:
- Database name: `app`
- User: `app`
- Read-write service: `${workspace_full_name}-db-rw`
- Supports workspace-to-workspace cloning (same user only)
- Backup bucket: `workspace-cnpg-${owner}-${name}-${short_id}`

### S3 Storage (Ceph)

When enabled, these environment variables are available:

```bash
S3_ENDPOINT        # https://s3.us-central-1.hahomelabs.com
S3_REGION          # us-central-1
S3_BUCKET          # workspace-${owner}-${name}-${short_id}
AWS_S3_ENDPOINT    # Same as S3_ENDPOINT
AWS_BUCKET         # Same as S3_BUCKET
S3_BACKUP_ENDPOINT # https://s3.us-central-1.hahomelabs.com
S3_BACKUP_BUCKET   # workspace-cnpg-${owner}-${name}-${short_id}
```

**S3 details**:
- Endpoint: `https://s3.us-central-1.hahomelabs.com`
- Region: `us-central-1`
- Max bucket size: 5GB
- Supports workspace-to-workspace cloning

### Convex Backend

When enabled:
- **Dashboard** (`/convex`): `https://convex--<workspace>--<user>.coder.hahomelabs.com`
- **API** (`/convex-api`): `https://convex-api--<workspace>--<user>.coder.hahomelabs.com`
- **Site Proxy** (`/convex-site`): `https://convex-site--<workspace>--<user>.coder.hahomelabs.com`
- **S3 Proxy** (`/convex-s3-proxy`): `https://convex-s3-proxy--<workspace>--<user>.coder.hahomelabs.com`
- Convex CLI available via `npx convex`
- Uses internal PostgreSQL and S3

### Nhost Backend

When enabled:
- **Dashboard** (`/nhost-dashboard`): `https://nhost-dashboard--<workspace>--<user>.coder.hahomelabs.com`
- **Hasura Console** (`/hasura`): `https://hasura--<workspace>--<user>.coder.hahomelabs.com`
- **MailHog** (`/mailhog`): `https://mailhog--<workspace>--<user>.coder.hahomelabs.com`
- **Auth** (hidden): `https://nhost-auth--<workspace>--<user>.coder.hahomelabs.com`
- **Functions** (hidden): `https://nhost-functions--<workspace>--<user>.coder.hahomelabs.com`
- **Storage** (hidden): `https://nhost-storage--<workspace>--<user>.coder.hahomelabs.com`
- **GraphQL** (hidden): `https://nhost-graphql--<workspace>--<user>.coder.hahomelabs.com`
- Uses internal PostgreSQL and S3

## LLM Gateway

AI requests route through LiteLLM proxy with budget controls:

```bash
# Environment variables (ask user before accessing)
OPENAI_BASE_URL      # https://llm-gateway.hahomelabs.com/v1
LITELLM_BASE_URL     # https://llm-gateway.hahomelabs.com
ANTHROPIC_AUTH_TOKEN # Per-user API key (development)
LITELLM_APP_API_KEY  # Per-user API key (applications)
```

**Model mapping**:
- Haiku → "small" (fast, low cost)
- Sonnet → "medium" (balanced)
- Opus → "large" (max capability)

## Package Managers

### System packages

```bash
sudo apt-get update
sudo apt-get install <package>
```

### Node.js

Check lockfile to determine which to use:
- `pnpm-lock.yaml` → Use `pnpm`
- `yarn.lock` → Use `yarn`
- `package-lock.json` → Use `npm`
- `bun.lockb` → Use `bun`

## Background Services

### PM2 (Node.js processes)

```bash
pm2 status          # Check status
pm2 logs            # View all logs
pm2 logs <app>      # View app logs
pm2 logs --lines 50 --nostream  # View recent log entries
pm2 restart <app>   # Restart app
```

### Docker

```bash
docker ps           # List containers
docker logs <container>
docker logs -f <container>  # Follow logs
```

## Workspace Scripts

| Script | Location | When it runs |
|--------|----------|--------------|
| Startup | `start.sh` | Workspace starts |
| Shutdown | `stop.sh` | Workspace stops |

Scripts are executed automatically by the Coder agent. Use them for:
- Starting development servers with PM2
- Running database migrations
- Setting up environment-specific configurations
- Graceful shutdown of services

**Note**: Startup script runs with 60-second timeout, then backgrounds if still running.

## Platform-Specific Considerations

### Docker Usage

- Docker commands work normally (this is not Docker Desktop)
- No special port mapping or host configurations needed
- Docker-in-Docker means containers run inside the workspace environment

### File Paths

- Use **standard Linux paths** (not Windows or macOS formats)
- **Relative paths** for project files: `src/components/Header.tsx`
- **Absolute paths** for system files: `/usr/local/bin/tool`

### Hardware Optimizations

- Target **x86_64 architecture** for any hardware-specific optimizations
- Do NOT use ARM/Apple Silicon-specific flags or binaries
- Modern Intel/AMD processor features are available

### Environment Variables

**CRITICAL**: Before using or changing ANY environment variable, you MUST:

1. **Ask the user for permission** - "May I check the environment variables?" or "May I use/change the X environment variable?"
2. **Explain what you need** - Describe which variable(s) you need to access and why
3. **Wait for explicit approval** - Do not proceed without user consent

To check available environment variables:
```bash
env | grep -i <pattern>    # Search for specific variables
env                        # List all environment variables
printenv                   # Alternative way to list all
echo $VAR_NAME             # Check specific variable
```

**Never** modify environment variables without explicit user permission, as they may affect:
- API authentication and routing
- Service connections
- Model selection behavior
- Workspace functionality

### Network Services

- Services run on **standard Linux ports**
- No macOS/Windows port conflicts to consider
- Internal cluster networking with port forwarding for external access

## Workspace Cloning

- **PostgreSQL cloning**: Restores from source workspace backup
- **S3 cloning**: Syncs data from source workspace bucket
- **Restriction**: Can only clone from own workspaces (same user)
- **Limitation**: Source workspace name cannot contain hyphens

## GitHub CLI

GitHub CLI (`gh`) is pre-configured with automatic OAuth token refresh. The token refreshes automatically via a wrapper function in `.bashrc`.

## Gotchas

1. **File paths**: Use standard Linux paths (`/home/coder/project`)
2. **Architecture**: x86_64 only (no ARM binaries)
3. **Environment variables**: Ask user before accessing
4. **Service URLs**: Use full URLs, not localhost
5. **Disk space**: Home directory is persistent, size configurable
6. **Workspace cloning**: Source workspaces with hyphens in name cannot be used
7. **Database**: PostgreSQL database name is always `app`, user is always `app`

## Capabilities

You can help with:

- **Code Development**: Writing, reviewing, and debugging code
- **Concept Explanations**: Explaining complex programming concepts
- **Best Practices**: Suggesting optimizations and patterns
- **Architecture**: Helping with design decisions
- **Troubleshooting**: Debugging technical issues
- **Documentation**: Providing comments and docs
- **DevOps**: Infrastructure and deployment tasks
- **Containers**: Docker and Kubernetes operations

## Response Guidelines

- Provide clear, concise, and accurate responses
- Consider the context of the workspace and the user's current task
- Account for the Linux x86_64 environment in all recommendations
- For Coder CLI commands and workspace management, reference the `coder-workspace-management` skill
