---
name: managing-railway
description: Railway platform CLI for service deployment, infrastructure management, and debugging. Use for creating services, managing deployments, configuring networking, and reviewing logs.
---

# Railway CLI Skill

Fast reference for Railway CLI operations. See [REFERENCE.md](REFERENCE.md) for comprehensive documentation.

---

## Overview

**What is Railway**: Modern PaaS for instant deployments with zero configuration. Supports any language/framework via Nixpacks or Dockerfile. Includes managed databases, private networking, and automatic SSL.

**When to Use**: Deploying apps, managing services/databases, debugging (logs, SSH), configuring domains, managing environment variables, CI/CD integration.

**Auto-Detection**: `railway.json`, `railway.toml`, `RAILWAY_TOKEN` in `.env`, or user mentions Railway.

---

## Table of Contents

1. [Overview](#overview)
2. [Critical: Avoiding Interactive Mode](#critical-avoiding-interactive-mode)
3. [Prerequisites](#prerequisites)
4. [Authentication](#authentication)
5. [CLI Decision Tree](#cli-decision-tree)
6. [Command Quick Reference](#command-quick-reference)
7. [Static Reference Data](#static-reference-data)
8. [Common Workflows](#common-workflows)
9. [Private Networking](#private-networking)
10. [Error Handling](#error-handling)
11. [Framework Quick Start](#framework-quick-start)
12. [JSON Output Mode](#json-output-mode)
13. [Quick Reference Card](#quick-reference-card)

---

## Critical: Avoiding Interactive Mode

**Railway CLI can enter interactive mode which will hang Claude Code.** Always use flags:

| Command | WRONG | CORRECT |
|---------|-------|---------|
| Link project | `railway link` | `railway link -p <project> -e <env>` |
| Create project | `railway init` | `railway init -n <name>` |
| Switch env | `railway environment` | `railway environment <name>` |
| Remove deploy | `railway down` | `railway down -y` |
| Redeploy | `railway redeploy` | `railway redeploy -y` |
| Deploy | `railway up` | `railway up --detach` |
| SSH | `railway ssh` | `railway ssh -- <command>` |

**Required flags**: `-y` (skip prompts), `--detach` (background), explicit names, `--json` (parsing), `-- <cmd>` (SSH).

**Never use**: `railway login`, `railway connect` (without service), `railway shell`, commands without explicit params.

---

## Prerequisites

```bash
# Verify installation
railway --version  # Expects: 3.x.x+

# Install options
npm i -g @railway/cli          # npm
brew install railway           # Homebrew
bash <(curl -fsSL cli.new)     # Shell script
```

---

## Authentication

### Token Types

| Token Type | Env Variable | Scope |
|------------|--------------|-------|
| **Project Token** | `RAILWAY_TOKEN` | Single environment (for `logs`, `up`) |
| Account Token | `RAILWAY_API_TOKEN` | All projects (for `init`, `link`) |

**Critical**: `railway logs` requires a **Project Token**, not an account token.

### Quick Setup

```bash
# Set token for session
export RAILWAY_TOKEN="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

# Or inline from .env
RAILWAY_TOKEN=$(grep RAILWAY_TOKEN .env | cut -d= -f2) railway logs

# Verify authentication
railway whoami
```

### Discovering Tokens

```bash
grep -i railway .env
grep -E '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}' .env
```

See [REFERENCE.md](REFERENCE.md#token-management) for token creation and storage best practices.

---

## CLI Decision Tree

### Project Operations
```
├── Create project      → railway init -n <name>
├── Link to project     → railway link -p <project> -e <env>
├── List projects       → railway list
├── View status         → railway status
└── Open dashboard      → railway open
```

### Deployment
```
├── Deploy (background) → railway up --detach
├── Redeploy            → railway redeploy -y
├── Remove deployment   → railway down -y
└── Deploy template     → railway deploy -t <template>
```

### Services & Databases
```
├── Add PostgreSQL      → railway add -d postgres
├── Add Redis           → railway add -d redis
├── Add from repo       → railway add -r owner/repo
├── Run with vars       → railway run <command>
└── Link to service     → railway service <name>
```

### Debugging
```
├── View logs           → railway logs
├── Build logs          → railway logs -b
├── SSH command         → railway ssh -- <command>
└── Check status        → railway status
```

### Environment & Variables
```
├── Switch environment  → railway environment <name>
├── Create environment  → railway environment new -d <source>
├── Delete environment  → railway environment delete <name> -y
├── View variables      → railway variables
└── Set variable        → railway variables --set KEY=value
```

See [REFERENCE.md](REFERENCE.md#complete-command-documentation) for all commands with full flag details.

---

## Command Quick Reference

### Project Management

| Command | Example |
|---------|---------|
| `railway init` | `railway init -n myapp` |
| `railway link` | `railway link -p myproject -e production` |
| `railway list` | `railway list` |
| `railway status` | `railway status` |
| `railway unlink` | `railway unlink` |

### Deployment

| Command | Example |
|---------|---------|
| `railway up` | `railway up --detach` |
| `railway redeploy` | `railway redeploy -y` |
| `railway down` | `railway down -y` |
| `railway logs` | `railway logs -d <id>` |

### Services

| Command | Example |
|---------|---------|
| `railway add` | `railway add -d postgres` |
| `railway service` | `railway service api` |
| `railway run` | `railway run npm start` |

### Debugging

| Command | Example |
|---------|---------|
| `railway logs` | `railway logs` |
| `railway logs -b` | `railway logs -b` |
| `railway ssh -- cmd` | `railway ssh -- ls -la` |

---

## Static Reference Data

### Regions

| Code | Location |
|------|----------|
| `us-west2` | California, USA |
| `us-east4-eqdc4a` | Virginia, USA |
| `europe-west4-drams3a` | Amsterdam, Netherlands |
| `asia-southeast1-eqsg3a` | Singapore |

### Database Types

| Type | Flag | Shell |
|------|------|-------|
| PostgreSQL | `-d postgres` | `psql` |
| MySQL | `-d mysql` | `mysql` |
| Redis | `-d redis` | `redis-cli` |
| MongoDB | `-d mongo` | `mongosh` |

### Railway-Provided Variables

| Variable | Description |
|----------|-------------|
| `RAILWAY_PUBLIC_DOMAIN` | Public domain |
| `RAILWAY_PRIVATE_DOMAIN` | Private domain (.railway.internal) |
| `PORT` | Port to listen on |
| `RAILWAY_ENVIRONMENT` | Environment name |

---

## Common Workflows

### 1. Deploy Application

```bash
railway init -n myapp                    # Create project
railway up --detach                      # Deploy (background)
railway logs                             # Check logs
```

### 2. Add Database

```bash
railway add -d postgres                  # Add PostgreSQL
railway run npm run migrate              # Run migrations
```

### 3. Configure Domain

```bash
railway domain                           # Generate Railway domain
railway domain api.myapp.com -p 3000     # Custom domain
```

### 4. Debug Failing Deployment

```bash
railway status                           # Check status
railway logs                             # View runtime logs
railway logs -b                          # View build logs
railway ssh -- ps aux                    # SSH command
```

### 5. CI/CD Deployment

```bash
export RAILWAY_TOKEN=${{ secrets.RAILWAY_TOKEN }}
railway up --detach -s api
```

See [REFERENCE.md](REFERENCE.md#cicd-integration) for GitHub Actions, GitLab CI, and CircleCI examples.

---

## Private Networking

Services communicate via: `<service-name>.railway.internal`

**Example**: `http://api.railway.internal:3000`

### Port Binding (Required)

Apps must listen on `::` for IPv4/IPv6:

```javascript
// Node.js
app.listen(process.env.PORT, '::', () => console.log('Running'));
```

```bash
# Python
gunicorn --bind "[::]:${PORT:-8000}" app:app
```

See [REFERENCE.md](REFERENCE.md#networking-deep-dive) for library configurations and TCP proxy.

---

## Error Handling

### Common Errors

| Error | Resolution |
|-------|------------|
| `command not found: railway` | Install via npm/brew |
| `Not logged in` | Set `RAILWAY_TOKEN` |
| `No project linked` | Run `railway link` |
| `Unauthorized` | Check token, re-authenticate |
| `Deployment failed` | Check `railway logs -b` |

### 502 Error Debugging

```bash
# 1. Get PROJECT token (not account token)
grep -i railway .env

# 2. Set token and verify
export RAILWAY_TOKEN="<uuid>"
railway whoami

# 3. Check logs
railway logs
```

**Common 502 causes**: Missing dependencies, port binding issues, startup crashes.

See [REFERENCE.md](REFERENCE.md#troubleshooting-deep-dive) for comprehensive troubleshooting.

---

## Framework Quick Start

### Node.js

```javascript
app.listen(process.env.PORT, '::', () => console.log('Running'));
```

### Python

```bash
# Procfile
web: gunicorn --bind "[::]:${PORT:-8000}" app:app
```

### Rails

```json
// railway.json
{
  "deploy": {
    "startCommand": "bundle exec rails server -b :: -p $PORT"
  }
}
```

See [REFERENCE.md](REFERENCE.md#config-as-code) for complete configuration options.

---

## JSON Output Mode

```bash
railway status --json | jq '.services[].name'
railway logs --json | jq -r 'select(.level == "error") | .message'
```

---

## Quick Reference Card

```bash
# Authentication
export RAILWAY_TOKEN="xxx"

# Project
railway init -n myapp
railway link -p myproject -e production
railway status

# Deploy
railway up --detach
railway redeploy -y
railway down -y

# Services
railway add -d postgres
railway run npm run migrate

# Debug
railway logs
railway logs -b
railway ssh -- ps aux

# Environment
railway environment staging
railway variables --set KEY=value

# Domain
railway domain api.example.com -p 3000
```

---

**See [REFERENCE.md](REFERENCE.md) for**: Complete command documentation, advanced deployment patterns, volume management, environment variable strategies, networking deep dive, CI/CD integration, security best practices, troubleshooting, and config-as-code.
