---
name: github-webhook-setup
description: |
  Configures GitHub webhooks for auto-deployment by verifying secrets, checking endpoint
  accessibility, and guiding configuration. Use when you need to add a new repo for
  auto-deploy, configure GitHub webhooks, set up continuous deployment, or troubleshoot
  webhook issues. Triggers on "setup webhook", "add webhook for [repo]", "configure
  auto-deploy", "GitHub deployment", or "webhook not working". Works with config/hooks.json,
  .env (WEBHOOK_SECRET), and webhook.temet.ai endpoint.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# GitHub Webhook Setup Skill

Configure GitHub webhooks for automatic deployment on push events.

## Quick Start

To add a new repo for auto-deployment:

1. Provide the repository name (e.g., "my-project")
2. Confirm the local project path exists on the server
3. Follow the GitHub webhook configuration steps

Example: "Set up webhook for my-project repo"

## Table of Contents

1. [When to Use This Skill](#1-when-to-use-this-skill)
2. [What This Skill Does](#2-what-this-skill-does)
3. [Instructions](#3-instructions)
   - 3.1 Verify WEBHOOK_SECRET
   - 3.2 Check Endpoint Accessibility
   - 3.3 Add Hook Configuration
   - 3.4 Guide GitHub Setup
   - 3.5 Test the Webhook
   - 3.6 Verify Deployment
4. [Supporting Files](#4-supporting-files)
5. [Expected Outcomes](#5-expected-outcomes)
6. [Requirements](#6-requirements)
7. [Red Flags to Avoid](#7-red-flags-to-avoid)

## When to Use This Skill

**Explicit Triggers:**
- "Set up webhook for [repo]"
- "Add GitHub auto-deploy for [repo]"
- "Configure webhook for [repository]"
- "New repo needs auto-deployment"

**Implicit Triggers:**
- Creating a new project that needs CI/CD
- Setting up a new service in the infrastructure
- Migrating a project to this server

**Debugging Triggers:**
- "Webhook not triggering"
- "Push event not deploying"
- "GitHub webhook returning 403/401"
- "Deployment not working"

## What This Skill Does

1. **Verifies Environment** - Checks WEBHOOK_SECRET exists (generates if needed)
2. **Tests Accessibility** - Confirms webhook.temet.ai endpoint responds
3. **Configures Hook** - Adds entry to hooks.json for the new repo
4. **Guides GitHub Setup** - Provides exact steps for GitHub webhook configuration
5. **Tests Integration** - Validates webhook receives events correctly
6. **Verifies Deployment** - Confirms push triggers deployment script

## Instructions

### 3.1 Verify WEBHOOK_SECRET

Check if WEBHOOK_SECRET exists in .env:

```bash
grep -E "^WEBHOOK_SECRET=" /home/dawiddutoit/projects/network/.env
```

**If missing or placeholder value, generate a new secret:**

```bash
openssl rand -hex 32
```

Add to .env:
```bash
WEBHOOK_SECRET=<generated-hex-string>
```

**Important:** After updating .env, restart the webhook container:
```bash
cd /home/dawiddutoit/projects/network && docker compose restart webhook
```

### 3.2 Check Endpoint Accessibility

Test the webhook health endpoint:

```bash
curl -I https://webhook.temet.ai/hooks/health
```

**Expected response:**
```
HTTP/2 200
content-type: text/plain; charset=utf-8
```

**If not accessible:**
1. Check Cloudflare tunnel is running: `docker ps | grep cloudflared`
2. Verify bypass policy exists for webhook.temet.ai
3. Check webhook container: `docker ps | grep webhook`
4. View webhook logs: `docker logs webhook --tail 50`

### 3.3 Add Hook Configuration

**Location:** `/home/dawiddutoit/projects/network/config/hooks.json`

**Template for new hook:**
```json
{
  "id": "<repo-name>",
  "execute-command": "/scripts/deploy.sh",
  "command-working-directory": "/projects/<repo-name>",
  "pass-arguments-to-command": [
    {
      "source": "payload",
      "name": "repository.full_name"
    }
  ],
  "trigger-rule": {
    "and": [
      {
        "match": {
          "type": "payload-hmac-sha256",
          "secret": "WEBHOOK_SECRET",
          "parameter": {
            "source": "header",
            "name": "X-Hub-Signature-256"
          }
        }
      },
      {
        "match": {
          "type": "value",
          "value": "refs/heads/main",
          "parameter": {
            "source": "payload",
            "name": "ref"
          }
        }
      }
    ]
  },
  "response-message": "Deployment triggered for <repo-name>"
}
```

**Key Fields:**
| Field | Description |
|-------|-------------|
| `id` | Hook identifier (used in webhook URL) |
| `command-working-directory` | Path where repo is cloned on server |
| `trigger-rule.match[1].value` | Branch to trigger on (usually `refs/heads/main`) |

**Steps to add:**
1. Read current hooks.json
2. Add new entry to the array (before closing `]`)
3. Restart webhook container: `docker compose restart webhook`

### 3.4 Guide GitHub Setup

Provide these exact instructions to the user:

```
GITHUB WEBHOOK CONFIGURATION

1. Go to your repository on GitHub
2. Click: Settings -> Webhooks -> Add webhook

3. Configure the webhook:
   - Payload URL: https://webhook.temet.ai/hooks/<repo-name>
   - Content type: application/json
   - Secret: <value-from-WEBHOOK_SECRET-in-.env>
   - SSL verification: Enable SSL verification (checked)

4. Events:
   - Select: "Just the push event"

5. Active: Checked

6. Click "Add webhook"
```

**Important:** The secret in GitHub MUST match WEBHOOK_SECRET in .env exactly.

### 3.5 Test the Webhook

**Option A: Push to trigger**
```bash
# Make a small change and push to main branch
git commit --allow-empty -m "Test webhook"
git push origin main
```

**Option B: GitHub UI test**
1. Go to repo Settings -> Webhooks
2. Click on the webhook
3. Go to "Recent Deliveries" tab
4. Click "Redeliver" on any delivery (or wait for a push)

**Check webhook received the event:**
```bash
docker logs webhook --tail 20
```

**Expected log output:**
```
[webhook] incoming HTTP request from X.X.X.X POST /hooks/<repo-name>
[webhook] <repo-name> got matched
[webhook] executing /scripts/deploy.sh
```

### 3.6 Verify Deployment

Check deployment script executed:

```bash
# View deploy logs
ls -la /tmp/deploy-*.log | tail -5

# Read latest deploy log
cat $(ls -t /tmp/deploy-*.log | head -1)
```

**Expected log content:**
```
[timestamp] === Deployment triggered for: owner/repo-name ===
[timestamp] Working directory: /projects/<repo-name>
[timestamp] Pulling latest changes...
[timestamp] Services updated successfully
[timestamp] === Deployment complete ===
```

**Verify git pulled latest:**
```bash
cd /projects/<repo-name> && git log -1 --oneline
```

## Supporting Files

| File | Purpose |
|------|---------|
| `references/reference.md` | Complete hooks.json schema, troubleshooting guide |
| `examples/examples.md` | Example configurations for different repo types |

## Expected Outcomes

**Success:**
- WEBHOOK_SECRET configured in .env
- hooks.json updated with new entry
- webhook.temet.ai/hooks/<repo-name> accessible
- GitHub webhook created and delivering
- Push events trigger deployment script
- Latest code pulled to server

**Partial Success:**
- Hook configured but GitHub not yet set up (user action needed)
- Webhook receiving but deployment script failing (check logs)

**Failure Indicators:**
- 401/403 from webhook endpoint -> Secret mismatch
- 404 from webhook endpoint -> Hook ID not in hooks.json
- "signature does not match" in logs -> Secret mismatch
- Deployment not running -> Check container logs

## Requirements

**Environment:**
- Docker running with webhook container
- Cloudflare tunnel connected
- webhook.temet.ai with bypass authentication
- WEBHOOK_SECRET in .env

**Server Setup:**
- Repository cloned to /projects/<repo-name>
- Git configured for pull operations
- Docker compose available (if repo has docker-compose.yml)

**GitHub:**
- Repository admin access (to create webhooks)
- Main branch exists

## Red Flags to Avoid

- [ ] Do not commit WEBHOOK_SECRET to git
- [ ] Do not use different secrets for different repos (one secret for all)
- [ ] Do not forget to restart webhook container after hooks.json changes
- [ ] Do not skip the health endpoint check
- [ ] Do not use HTTP (always HTTPS via tunnel)
- [ ] Do not add hooks for branches other than main without updating trigger-rule
- [ ] Do not skip testing with an actual push event
- [ ] Do not forget to clone the repo to /projects/ on the server first

## Notes

- The webhook container reads WEBHOOK_SECRET as environment variable, referenced in hooks.json as "WEBHOOK_SECRET" (not the actual value)
- All repos share the same WEBHOOK_SECRET for simplicity
- The deploy.sh script is generic and works for any repo with docker-compose.yml
- Webhook endpoint has Cloudflare Access bypass (public access for GitHub)
- Deploy logs are written to /tmp/ with timestamps
- The health endpoint (/hooks/health) is useful for monitoring
