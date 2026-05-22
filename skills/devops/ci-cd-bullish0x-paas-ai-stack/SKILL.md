---
name: ci-cd-setup
description: Set up CI/CD pipelines - connect Gitea repos to Coolify using deploy keys and webhooks (official Coolify approach).
metadata: {"moltbot":{"emoji":"🔄","requires":{"env":["GITEA_TOKEN","COOLIFY_TOKEN"]}}}
---

# CI/CD Pipeline Setup Skill

This skill automates connecting Gitea repositories to Coolify for continuous deployment using the **official Coolify integration method**.

## Quick Reference

```bash
# Connect a repo to Coolify (one command - handles everything)
bash /srv/paas/scripts/setup-ci-cd.sh <repo-name> <subdomain> [port]

# Example: Deploy "my-api" at https://api.digpulsepi.com
bash /srv/paas/scripts/setup-ci-cd.sh my-api api 8080
```

**Required env vars**: `GITEA_TOKEN`, `COOLIFY_TOKEN`

## How CI/CD Works (Official Coolify Method)

```
┌─────────────────────────────────────────────────────────────────┐
│                    CI/CD FLOW                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. git push to Gitea                                           │
│           ↓                                                     │
│  2. Gitea sends webhook to Coolify                              │
│     URL: https://coolify.{domain}/webhooks/source/gitea/        │
│          events/manual?app={APP_UUID}                           │
│           ↓                                                     │
│  3. Coolify verifies webhook secret (manual_webhook_secret_gitea)│
│           ↓                                                     │
│  4. Coolify helper container clones via SSH                     │
│     git@gitea:user/repo.git (uses deploy key)                   │
│           ↓                                                     │
│  5. Build & Deploy container                                    │
│           ↓                                                     │
│  6. Traefik routes traffic to container                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Prerequisites

### Verify Network Connectivity

The stack uses two bridged networks. All core services must be on BOTH for full functionality:

```bash
# Check service networks
for svc in gitea n8n openclaw-cli lobe-chat; do
    echo "$svc: $(docker inspect $svc --format '{{range $k, $v := .NetworkSettings.Networks}}{{$k}} {{end}}')"
done

# Required: Gitea on coolify network (for Coolify helper to clone repos via SSH)
docker inspect gitea --format '{{range $k, $v := .NetworkSettings.Networks}}{{$k}} {{end}}' | grep coolify

# If missing, connect all services:
docker network connect coolify gitea
docker network connect coolify n8n
docker network connect coolify openclaw-cli
docker network connect coolify lobe-chat
docker network connect paas-network coolify-proxy
```

### Verify API Tokens

```bash
# Test Gitea token
curl -sf "http://127.0.0.1:3000/api/v1/user" \
  -H "Authorization: token $GITEA_TOKEN" | jq '{login, email}'

# Test Coolify token  
curl -sf "http://127.0.0.1:8080/api/v1/servers" \
  -H "Authorization: Bearer $COOLIFY_TOKEN" | jq '.[0].name'
```

## Automated Setup (Recommended)

```bash
# Export tokens (if not already in environment)
export GITEA_TOKEN="your-gitea-token"
export COOLIFY_TOKEN="your-coolify-token"

# Run setup script
bash /srv/paas/scripts/setup-ci-cd.sh REPO_NAME SUBDOMAIN PORT
```

The script handles:
1. ✅ Creates repository in Gitea (if needed)
2. ✅ Generates SSH deploy key pair
3. ✅ Adds private key to Coolify via API
4. ✅ Adds public key to Gitea repo as deploy key
5. ✅ Creates application in Coolify with `private-deploy-key` endpoint
6. ✅ Creates webhook in Gitea with matching secret
7. ✅ Sets `is_force_https_enabled: false` (Cloudflare handles HTTPS)

## Manual Setup (Step by Step)

### Step 1: Generate SSH Deploy Key

```bash
KEY_NAME="my-app-deploy-key"
ssh-keygen -t ed25519 -f "$KEY_NAME" -N "" -C "$KEY_NAME"
```

### Step 2: Add Private Key to Coolify

```bash
PRIVATE_KEY=$(cat "$KEY_NAME" | jq -Rs .)

curl -sf -X POST "http://127.0.0.1:8080/api/v1/security/keys" \
  -H "Authorization: Bearer $COOLIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"$KEY_NAME\",
    \"description\": \"Deploy key for my-app\",
    \"private_key\": $PRIVATE_KEY
  }"
# Returns: {"uuid": "KEY_UUID"}
```

### Step 3: Add Public Key to Gitea Repository

```bash
PUBLIC_KEY=$(cat "${KEY_NAME}.pub")

curl -sf -X POST "http://127.0.0.1:3000/api/v1/repos/OWNER/REPO/keys" \
  -H "Authorization: token $GITEA_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"$KEY_NAME\",
    \"key\": \"$PUBLIC_KEY\",
    \"read_only\": true
  }"
```

### Step 4: Get Coolify UUIDs

```bash
# Server UUID
SERVER_UUID=$(curl -sf "http://127.0.0.1:8080/api/v1/servers" \
  -H "Authorization: Bearer $COOLIFY_TOKEN" | jq -r '.[0].uuid')

# Project UUID
PROJECT_UUID=$(curl -sf "http://127.0.0.1:8080/api/v1/projects" \
  -H "Authorization: Bearer $COOLIFY_TOKEN" | jq -r '.[0].uuid')

echo "Server: $SERVER_UUID"
echo "Project: $PROJECT_UUID"
```

### Step 5: Create Application with Deploy Key

```bash
# Generate webhook secret
WEBHOOK_SECRET=$(openssl rand -hex 16)

curl -sf -X POST "http://127.0.0.1:8080/api/v1/applications/private-deploy-key" \
  -H "Authorization: Bearer $COOLIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"project_uuid\": \"$PROJECT_UUID\",
    \"server_uuid\": \"$SERVER_UUID\",
    \"environment_name\": \"production\",
    \"private_key_uuid\": \"$KEY_UUID\",
    \"git_repository\": \"git@gitea:OWNER/REPO.git\",
    \"git_branch\": \"main\",
    \"name\": \"my-app\",
    \"description\": \"Deployed from Gitea\",
    \"domains\": \"http://myapp.digpulsepi.com\",
    \"ports_exposes\": \"80\",
    \"build_pack\": \"dockerfile\",
    \"is_auto_deploy_enabled\": true,
    \"is_force_https_enabled\": false,
    \"manual_webhook_secret_gitea\": \"$WEBHOOK_SECRET\",
    \"instant_deploy\": false
  }"
# Returns: {"uuid": "APP_UUID"}
```

**Important Notes:**
- Use `http://` for domains (Cloudflare handles HTTPS)
- `is_force_https_enabled: false` prevents redirect loops
- `manual_webhook_secret_gitea` must match webhook secret in Gitea
- Git URL uses internal hostname: `git@gitea:user/repo.git`

### Step 6: Create Webhook in Gitea

```bash
# Webhook URL format (official Coolify format)
WEBHOOK_URL="https://coolify.digpulsepi.com/webhooks/source/gitea/events/manual?app=$APP_UUID"

curl -sf -X POST "http://127.0.0.1:3000/api/v1/repos/OWNER/REPO/hooks" \
  -H "Authorization: token $GITEA_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"active\": true,
    \"type\": \"gitea\",
    \"config\": {
      \"url\": \"$WEBHOOK_URL\",
      \"content_type\": \"json\",
      \"secret\": \"$WEBHOOK_SECRET\"
    },
    \"events\": [\"push\", \"pull_request\"],
    \"branch_filter\": \"*\"
  }"
```

### Step 7: Trigger First Deployment

```bash
# Trigger deployment via API
curl -sf -X POST "http://127.0.0.1:8080/api/v1/applications/$APP_UUID/restart" \
  -H "Authorization: Bearer $COOLIFY_TOKEN"

# Check deployment status
curl -sf "http://127.0.0.1:8080/api/v1/deployments" \
  -H "Authorization: Bearer $COOLIFY_TOKEN" | jq '.[0] | {uuid, status}'
```

## Troubleshooting

### Deployment fails: "Could not resolve hostname gitea"

```bash
# Connect all core services to coolify network
docker network connect coolify gitea
docker network connect coolify n8n
docker network connect coolify openclaw-cli
docker network connect coolify lobe-chat
docker network connect paas-network coolify-proxy
```

### Webhook not triggering deployment

```bash
# Check webhook exists in Gitea
curl -sf "http://127.0.0.1:3000/api/v1/repos/OWNER/REPO/hooks" \
  -H "Authorization: token $GITEA_TOKEN" | jq '.[] | {id, active, config}'

# Verify webhook secret matches in Coolify app
curl -sf "http://127.0.0.1:8080/api/v1/applications/$APP_UUID" \
  -H "Authorization: Bearer $COOLIFY_TOKEN" | jq '.manual_webhook_secret_gitea'
```

### Test webhook manually

```bash
# Simulate a push event
curl -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -H "X-Gitea-Event: push" \
  -H "X-Gitea-Signature: $(echo -n '{}' | openssl dgst -sha256 -hmac '$WEBHOOK_SECRET' | cut -d' ' -f2)" \
  -d '{}'
```

### Check deployment logs

```bash
# Get latest deployment
DEPLOY_UUID=$(curl -sf "http://127.0.0.1:8080/api/v1/deployments" \
  -H "Authorization: Bearer $COOLIFY_TOKEN" | jq -r '.[0].uuid')

# Check status
curl -sf "http://127.0.0.1:8080/api/v1/deployments/$DEPLOY_UUID" \
  -H "Authorization: Bearer $COOLIFY_TOKEN" | jq '{status, created_at, finished_at}'
```

## API Reference

### Coolify Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/applications/private-deploy-key` | POST | Create app with deploy key |
| `/api/v1/applications/{uuid}/restart` | POST | Trigger deployment |
| `/api/v1/security/keys` | POST | Add SSH private key |
| `/api/v1/deployments/{uuid}` | GET | Check deployment status |
| `/webhooks/source/gitea/events/manual?app={uuid}` | POST | Webhook endpoint |

### Gitea Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/repos/{owner}/{repo}/keys` | POST | Add deploy key |
| `/api/v1/repos/{owner}/{repo}/hooks` | POST | Create webhook |

### Build Packs

| Build Pack | Use Case |
|------------|----------|
| `dockerfile` | Has Dockerfile (recommended) |
| `nixpacks` | Auto-detect language |
| `dockercompose` | Multi-container apps |
| `static` | HTML/CSS/JS only |
