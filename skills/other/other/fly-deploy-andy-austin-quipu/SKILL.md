---
name: fly-deploy
description: Deploy, manage, and troubleshoot Fly.io applications for the Quipu project (Brain and Hands services). Use when the user mentions Fly.io, fly deploy, deployment, secrets, scaling, logs, machines, or production infrastructure. Covers deploying both services, managing secrets, monitoring, and internal networking.
---

# Fly.io Deployment Skill

This skill manages deployment and operations for the Quipu project's two Fly.io services:

- **Brain** (`brain/`) — Public-facing FastAPI agent API
- **Hands** (`hands/`) — Internal-only FastMCP tool server

## Project Service Map

| Service | Fly App | Port | Visibility | Config |
|---------|---------|------|------------|--------|
| Brain | `quipu-brain` | 8000 | Public (HTTPS) | `brain/fly.toml` |
| Hands | `quipu-hands` | 8080 | Internal only | `hands/fly.toml` |

Internal communication: `http://quipu-hands.internal:8080/sse`

## Prerequisites

```bash
# Install Fly CLI
brew install flyctl

# Authenticate
fly auth login
```

## First-Time Setup

### 1. Create Apps

```bash
fly apps create quipu-hands
fly apps create quipu-brain
```

### 2. Set Secrets

Always deploy Hands first since the Brain depends on it.

```bash
# Hands secrets
fly secrets set \
  SUPABASE_DB_URL="postgresql://..." \
  -a quipu-hands

# Brain secrets
fly secrets set \
  GOOGLE_API_KEY="..." \
  SUPABASE_JWT_SECRET="..." \
  MCP_SERVER_URL="http://quipu-hands.internal:8080/sse" \
  -a quipu-brain
```

### 3. Deploy

```bash
# Deploy Hands first (Brain depends on it)
fly deploy -a quipu-hands --config hands/fly.toml --dockerfile hands/Dockerfile

# Then deploy Brain
fly deploy -a quipu-brain --config brain/fly.toml --dockerfile brain/Dockerfile
```

## Common Operations

### Deploy Both Services

Always deploy Hands before Brain when both need updating:

```bash
fly deploy -a quipu-hands --config hands/fly.toml --dockerfile hands/Dockerfile && \
fly deploy -a quipu-brain --config brain/fly.toml --dockerfile brain/Dockerfile
```

### Deploy Single Service

```bash
# Brain only
fly deploy -a quipu-brain --config brain/fly.toml --dockerfile brain/Dockerfile

# Hands only
fly deploy -a quipu-hands --config hands/fly.toml --dockerfile hands/Dockerfile
```

### View Logs

```bash
# Brain logs
fly logs -a quipu-brain

# Hands logs
fly logs -a quipu-hands
```

### Check Status

```bash
fly status -a quipu-brain
fly status -a quipu-hands
```

### SSH Into Running Machine

```bash
fly ssh console -a quipu-brain
fly ssh console -a quipu-hands
```

### Manage Secrets

```bash
# List secrets
fly secrets list -a quipu-brain

# Update a secret (triggers redeployment)
fly secrets set GOOGLE_API_KEY="new-key" -a quipu-brain

# Stage a secret without redeploying
fly secrets set GOOGLE_API_KEY="new-key" --stage -a quipu-brain
fly secrets deploy -a quipu-brain

# Remove a secret
fly secrets unset SECRET_NAME -a quipu-brain
```

### Scale Machines

```bash
# Scale Brain to 2 machines
fly scale count 2 -a quipu-brain

# Check current scale
fly scale show -a quipu-brain
```

## Networking

The Brain reaches the Hands via Fly's private IPv6 network using the `.internal` TLD:

```
MCP_SERVER_URL=http://quipu-hands.internal:8080/sse
```

This means:
- No public IP needed for Hands
- All MCP traffic stays within Fly's network
- Low latency between services
- The Hands service is not accessible from the internet

## Health Checks

Both services have health checks configured in their `fly.toml`:

- Brain: `GET /health` every 30s
- Hands: No explicit health check (auto-start/stop based on connections)

Verify remotely:

```bash
# Brain (public)
curl https://quipu-brain.fly.dev/health

# Hands (must SSH or use fly proxy)
fly proxy 18080:8080 -a quipu-hands
curl http://localhost:18080/sse
```

## Troubleshooting

### Brain can't connect to Hands

1. Verify Hands is running: `fly status -a quipu-hands`
2. Check the MCP_SERVER_URL secret: `fly secrets list -a quipu-brain`
3. Ensure both apps are in the same Fly organization
4. Check Hands logs for startup errors: `fly logs -a quipu-hands`

### Deployment fails

1. Check build logs: `fly deploy -a quipu-brain --config brain/fly.toml --dockerfile brain/Dockerfile --verbose`
2. Verify Dockerfile builds locally: `docker build -f brain/Dockerfile brain/`
3. Check machine resources: `fly scale show -a quipu-brain`

### App not responding

1. Check if machines are running: `fly status -a quipu-brain`
2. Review recent logs: `fly logs -a quipu-brain`
3. Restart machines: `fly apps restart quipu-brain`

## Fly MCP Server

Fly.io has a built-in MCP server for managing infrastructure from Claude Code:

```bash
fly mcp server --claude
```

This enables managing Fly apps through natural language in Claude Code.