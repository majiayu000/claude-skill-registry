---
name: paas-overview
description: Overview of the PaaS stack - health checks, service URLs, and common operations.
metadata: {"moltbot":{"emoji":"🏠","requires":{"env":["GITEA_TOKEN","COOLIFY_TOKEN","N8N_TOKEN"]}}}
---

# PaaS Stack Overview

This skill provides an overview of the self-hosted PaaS stack and common operations.

## Services

| Service | Purpose | Env Vars |
|---------|---------|----------|
| Gitea | Git repository hosting | `GITEA_TOKEN`, `GITEA_URL` |
| Coolify | Application deployment | `COOLIFY_TOKEN`, `COOLIFY_URL` |
| n8n | Workflow automation | `N8N_TOKEN`, `N8N_URL` |
| LobeChat | AI chat interface | `LOBE_URL` |
| OpenClaw | AI gateway | `OPENCLAW_GATEWAY_TOKEN` |

## Quick Health Check

```bash
echo "=== Service Health ==="
echo "Gitea: $(curl -sf $GITEA_URL/api/healthz && echo OK || echo FAIL)"
echo "Coolify: $(curl -sf $COOLIFY_URL/api/health && echo OK || echo FAIL)"
echo "n8n: $(curl -sf $N8N_URL/healthz && echo OK || echo FAIL)"
echo "LobeChat: $(curl -sf $LOBE_URL/api/health && echo OK || echo FAIL)"
```

## Available Skills

| Skill | Purpose | Quick Command |
|-------|---------|---------------|
| `gitea` | Repository management | List repos, create branches, manage PRs |
| `coolify` | Deployment management | Deploy apps, manage envs, view logs |
| `n8n` | Workflow automation | Create workflows, manage credentials |
| `ci-cd` | CI/CD pipeline setup | Connect repos to Coolify |
| `lobechat` | LobeChat integration | Knowledge base queries |

## Common Operations

### Create and Deploy a New App

```bash
# 1. Create repository in Gitea
curl -X POST "$GITEA_URL/api/v1/user/repos" \
  -H "Authorization: token $GITEA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "my-app", "auto_init": true}'

# 2. Connect to Coolify (creates deploy key + webhook)
bash /srv/paas/scripts/setup-ci-cd.sh my-app myapp 3000

# 3. Push code → auto deploys via webhook
```

### CI/CD Architecture

```
Push to Gitea
    ↓
Webhook → https://coolify.domain/webhooks/source/gitea/events/manual?app={uuid}
    ↓
Coolify clones via SSH (git@gitea:user/repo.git)
    ↓
Build container → Deploy to coolify network
    ↓
Traefik routes by domain → Container
```

**Key requirements:**
- Gitea must be on `coolify` network (for SSH clone access)
- Coolify proxy must be on `paas-network` (for cloudflared access)
- Deploy key in both Coolify and Gitea
- Webhook secret matching `manual_webhook_secret_gitea`

### Check Deployment Status

```bash
curl -s "$COOLIFY_URL/api/v1/deployments" \
  -H "Authorization: Bearer $COOLIFY_TOKEN" | jq '.[0:3] | .[] | {status, created_at}'
```

### Trigger Manual Deployment

```bash
curl -X POST "$COOLIFY_URL/api/v1/applications/APP_UUID/restart" \
  -H "Authorization: Bearer $COOLIFY_TOKEN"
```

### Create Automation Workflow

```bash
# List n8n workflows
curl -s "$N8N_URL/api/v1/workflows" \
  -H "X-N8N-API-KEY: $N8N_TOKEN" | jq '.data[] | {id, name, active}'
```

## Scripts

| Script | Purpose |
|--------|---------|
| `bash /srv/paas/scripts/setup-ci-cd.sh` | Connect repo → Coolify with deploy keys |
| `bash /srv/paas/scripts/refresh-tokens.sh` | Regenerate API tokens |
| `bash /srv/paas/scripts/bootstrap.sh` | Full stack setup |

**Note:** Use `bash` prefix for cross-platform compatibility.

## Token Refresh

If API calls fail with authentication errors:

```bash
# Refresh all tokens
bash /srv/paas/scripts/refresh-tokens.sh --all

# Refresh specific service
bash /srv/paas/scripts/refresh-tokens.sh --gitea
bash /srv/paas/scripts/refresh-tokens.sh --coolify
```

## Network Architecture

The stack uses two bridged networks for full inter-service communication:

| Network | Services | Purpose |
|---------|----------|---------|
| `paas-network` | All core services | Stack internal communication |
| `coolify` | Deployed apps + proxy | Coolify-managed applications |

**All core services are connected to BOTH networks**, allowing:
- Stack services to communicate with each other
- Stack services to communicate with deployed applications
- n8n workflows to call deployed app APIs
- OpenClaw agent to interact with deployed services

## Network Troubleshooting

```bash
# Check which networks a service is on
docker inspect gitea --format '{{range $k, $v := .NetworkSettings.Networks}}{{$k}} {{end}}'

# Connect all core services to coolify network (if missing)
docker network connect coolify gitea
docker network connect coolify n8n
docker network connect coolify openclaw-cli
docker network connect coolify lobe-chat
docker network connect paas-network coolify-proxy

# Verify all connections
for svc in gitea n8n openclaw-cli lobe-chat; do
    echo "$svc: $(docker inspect $svc --format '{{range $k, $v := .NetworkSettings.Networks}}{{$k}} {{end}}')"
done
```

## Service-Specific Skills

For detailed operations, use the dedicated skills:

- **Gitea operations**: Read `/srv/paas/skills/gitea/SKILL.md`
- **Coolify operations**: Read `/srv/paas/skills/coolify/SKILL.md`
- **n8n operations**: Read `/srv/paas/skills/n8n/SKILL.md`
- **CI/CD setup**: Read `/srv/paas/skills/ci-cd/SKILL.md`

## Environment Variables

All service URLs and tokens are available as environment variables:

```bash
# Check available env vars
env | grep -E "_URL|_TOKEN" | grep -v "="
```
