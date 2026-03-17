---
name: deploy
description: |
  Deploy projects to staging or production environments. Repo-agnostic deployment
  orchestration using SSH MCP for VPS operations and Cloudflare for DNS/SSL.
  Reads project configuration from deployments.registry.json.
examples:
  - "/deploy"
  - "/deploy staging"
  - "/deploy production --project=tribevibe"
  - "/deploy status"
  - "/deploy rollback"
---

# Infrastructure Deployment Skill

Deploy any registered project to staging or production environments with full verification.

## Prerequisites

- SSH MCP configured for target VPS (passphrase-free keys)
- Docker + docker-compose on VPS
- Cloudflare CLI (wrangler) for DNS operations
- Project registered in `deployments.registry.json`

## Usage

```bash
/deploy                          # Interactive: select project + environment
/deploy staging                  # Deploy current project to staging
/deploy production               # Deploy current project to production
/deploy status                   # Check deployment status across all projects
/deploy rollback                 # Rollback last deployment
/deploy --project=tribevibe staging   # Deploy specific project
```

## Configuration

Projects are defined in `.claude-toolkit/.claude/skills/infrastructure/deployments.registry.json`:

```json
{
  "projects": {
    "projectname": {
      "vps": { "host": "x.x.x.x", "user": "root", "sshKeyName": "key_name" },
      "environments": {
        "staging": { "domain": "...", "dockerCompose": "..." },
        "production": { "domain": "...", "dockerCompose": "..." }
      }
    }
  }
}
```

## Workflow

### 1. Pre-Deployment Checks

```bash
# Read registry to get project config
REGISTRY=".claude-toolkit/.claude/skills/infrastructure/deployments.registry.json"

# Detect current project from git remote or CLAUDE.md
PROJECT=$(git remote get-url origin | grep -oP '(?<=/)[^/]+(?=\.git)')

# Verify VPS connectivity
ssh -o ConnectTimeout=5 ${USER}@${HOST} "echo 'VPS accessible'"

# Verify Docker is running
ssh ${USER}@${HOST} "docker info > /dev/null 2>&1"
```

### 2. Build & Push (if using CI)

```bash
# Trigger GitHub Actions deployment workflow
gh workflow run deploy-${ENV}.yml --ref ${BRANCH}

# Or build locally and push
docker build -t ${PROJECT}-api:${VERSION} .
docker push ghcr.io/${ORG}/${PROJECT}-api:${VERSION}
```

### 3. Deploy to VPS

```bash
# SSH to VPS and deploy
ssh ${USER}@${HOST} << 'DEPLOY'
  cd ${DOCKER_COMPOSE_PATH}

  # Backup database before deployment
  docker exec ${DB_CONTAINER} pg_dump -U postgres ${DB_NAME} > /backup/${PROJECT}_$(date +%Y%m%d_%H%M%S).sql

  # Pull latest images
  docker compose pull

  # Rolling restart (zero-downtime if configured)
  docker compose up -d --remove-orphans

  # Wait for health checks
  sleep 10
  docker compose ps
DEPLOY
```

### 4. Post-Deployment Verification

```bash
# Health check
curl -f https://${API_DOMAIN}/health || echo "FAILED"

# Check container status
ssh ${USER}@${HOST} "docker ps --format 'table {{.Names}}\t{{.Status}}'"

# Check recent logs for errors
ssh ${USER}@${HOST} "docker logs ${API_CONTAINER} --tail 50 | grep -i error"
```

### 5. Rollback (if needed)

```bash
# Rollback to previous image
ssh ${USER}@${HOST} << 'ROLLBACK'
  cd ${DOCKER_COMPOSE_PATH}
  docker compose down
  docker tag ${PROJECT}-api:previous ${PROJECT}-api:latest
  docker compose up -d
ROLLBACK

# Or restore database
ssh ${USER}@${HOST} "cat /backup/${PROJECT}_LATEST.sql | docker exec -i ${DB_CONTAINER} psql -U postgres ${DB_NAME}"
```

## MCP Integration

This skill uses SSH MCP for secure VPS access:

```json
{
  "id": "project-vps",
  "command": "npx ssh-mcp",
  "args": ["--host=${HOST}", "--user=${USER}", "--key=${SSH_KEY_PATH}"]
}
```

Tool reference: `mcp__project-vps__exec`

## Safety Rules

- NEVER deploy to production without staging verification first
- ALWAYS backup database before deployment
- ALWAYS verify health checks after deployment
- NEVER skip rollback plan
- ALWAYS monitor logs for 10-15 minutes post-deploy

## Output Format

```markdown
# Deployment Report

**Project**: ${project}
**Environment**: ${environment}
**Status**: SUCCESS | FAILED | ROLLED_BACK

## Services
| Service | Status | Health |
|---------|--------|--------|
| api     | Up 2m  | 200 OK |
| web     | Up 2m  | 200 OK |
| db      | Up 5h  | Connected |

## Health Checks
- API: https://api.example.com/health - 200 OK (45ms)
- Web: https://example.com - 200 OK (120ms)

## Actions Taken
1. Pulled latest images
2. Backed up database
3. Deployed via docker compose
4. Verified health checks

## Next Steps
- Monitor Seq logs: https://seq.example.com
- Run smoke tests
```
