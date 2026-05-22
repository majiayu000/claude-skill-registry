---
name: managing-vercel
description: Vercel platform CLI for frontend deployments, serverless functions, and edge network management. Use for deploying applications, managing domains, environment variables, and debugging deployments.
---

# Vercel CLI Skill

**Purpose**: Fast reference for Vercel CLI operations | **Target**: <500 lines

---

## Overview

**What is Vercel**: Frontend cloud platform with automatic CI/CD, serverless functions, edge network, and global CDN. Optimized for Next.js, React, Vue, and other frameworks.

**When to Use**:
- Deploying frontend applications
- Managing serverless functions and domains
- Managing environment variables
- Debugging deployments and logs

**Auto-Detection Triggers**:
- `vercel.json` in project root
- `.vercel` directory present
- `VERCEL_TOKEN` in `.env` file

**Progressive Disclosure**:
- **This file**: Quick reference for immediate use
- **[REFERENCE.md](./REFERENCE.md)**: Advanced patterns, CI/CD, troubleshooting deep-dives

---

## Table of Contents

1. [Critical: Avoiding Interactive Mode](#critical-avoiding-interactive-mode)
2. [Prerequisites](#prerequisites)
3. [Authentication](#authentication)
4. [CLI Decision Tree](#cli-decision-tree)
5. [Command Reference](#command-reference)
6. [Static Reference Data](#static-reference-data)
7. [Common Workflows](#common-workflows)
8. [Error Handling](#error-handling)
9. [Framework Examples](#framework-examples)
10. [Agent Integration](#agent-integration)
11. [Quick Reference Card](#quick-reference-card)

---

## Critical: Avoiding Interactive Mode

**Vercel CLI can hang Claude Code.** Always use flags to bypass prompts:

| Command | WRONG | CORRECT |
|---------|-------|---------|
| Deploy | `vercel` | `vercel --yes --token $VERCEL_TOKEN` |
| Link | `vercel link` | `vercel link --yes --project <name>` |
| Pull env | `vercel pull` | `vercel pull --yes --environment production` |
| Add env | `vercel env add` | `vercel env add NAME production < value.txt` |
| Remove | `vercel env rm NAME` | `vercel env rm NAME --yes` |

**Required flags**: `--yes`, `--token <TOKEN>`, explicit names, `--no-wait`

**Never use**: `vercel login`, `vercel dev`, commands without `--yes` when modifying

---

## Prerequisites

```bash
# Check CLI
vercel --version  # Expects: 30.x.x+

# Install
npm i -g vercel
```

---

## Authentication

| Token Type | Scope | Use Case |
|------------|-------|----------|
| Personal | Full account | CI/CD, automation |
| Team | Team-scoped | Team deployments |
| Project | Project-scoped | Limited access |

```bash
# Set token from .env
export VERCEL_TOKEN="$(grep VERCEL_TOKEN .env | cut -d= -f2)"
vercel --token $VERCEL_TOKEN whoami
```

---

## CLI Decision Tree

### Project Operations
```
Link to project      --> vercel link --yes --project <name>
List projects        --> vercel project ls
Create project       --> vercel project add <name>
Remove project       --> vercel project rm <name> --yes
Current user         --> vercel whoami
Switch teams         --> vercel switch <team-slug>
```

### Deployment Operations
```
Deploy preview       --> vercel --yes
Deploy production    --> vercel --prod --yes
Staged production    --> vercel --prod --skip-domain --yes
Promote staged       --> vercel promote <url> --yes
Redeploy existing    --> vercel redeploy <url> --no-wait
Rollback             --> vercel rollback <url>
List deployments     --> vercel list [project]
Inspect deployment   --> vercel inspect <url>
Remove deployment    --> vercel remove <url> --yes
```

### Environment Variables
```
List vars            --> vercel env ls [environment]
Add var              --> echo "value" | vercel env add NAME production
Add from file        --> vercel env add NAME production < secret.txt
Remove var           --> vercel env rm NAME --yes
Pull to .env         --> vercel pull --yes --environment production
```

### Domains
```
List domains         --> vercel domains ls
Add domain           --> vercel domains add <domain> [project]
Force add            --> vercel domains add <domain> <project> --force
Remove domain        --> vercel domains rm <domain> --yes
Inspect domain       --> vercel domains inspect <domain>
```

### Debugging
```
View logs            --> vercel logs <deployment-url>
Logs as JSON         --> vercel logs <url> --json
Inspect details      --> vercel inspect <url>
HTTP status          --> vercel httpstat <url>
```

> For DNS, certificates, and advanced operations, see [REFERENCE.md](./REFERENCE.md#complete-command-documentation)

---

## Command Reference

### Core Commands

| Command | Description | Example |
|---------|-------------|---------|
| `vercel` | Deploy preview | `vercel --yes` |
| `vercel --prod` | Deploy production | `vercel --prod --yes` |
| `vercel link` | Link to project | `vercel link --yes --project myapp` |
| `vercel project ls` | List projects | `vercel project ls --json` |
| `vercel list` | List deployments | `vercel list --json` |
| `vercel logs` | View logs | `vercel logs <url>` |
| `vercel inspect` | Deployment details | `vercel inspect <url>` |

### Environment Variables

| Command | Description | Example |
|---------|-------------|---------|
| `vercel env ls` | List variables | `vercel env ls production` |
| `vercel env add` | Add variable | `echo "val" \| vercel env add KEY prod` |
| `vercel env rm` | Remove variable | `vercel env rm KEY --yes` |
| `vercel pull` | Pull env + settings | `vercel pull --yes --environment prod` |

### Domains

| Command | Description | Example |
|---------|-------------|---------|
| `vercel domains ls` | List domains | `vercel domains ls` |
| `vercel domains add` | Add domain | `vercel domains add api.example.com myapp` |
| `vercel domains rm` | Remove domain | `vercel domains rm api.example.com --yes` |

---

## Static Reference Data

### Deployment Regions (Key Regions)

| Code | Location | AWS Region |
|------|----------|------------|
| `iad1` | Washington DC (default) | us-east-1 |
| `sfo1` | San Francisco | us-west-1 |
| `fra1` | Frankfurt | eu-central-1 |
| `lhr1` | London | eu-west-2 |
| `hnd1` | Tokyo | ap-northeast-1 |
| `sin1` | Singapore | ap-southeast-1 |
| `syd1` | Sydney | ap-southeast-2 |

> Full 19-region list in [REFERENCE.md](./REFERENCE.md#multi-region-configuration)

### Environment Types

| Environment | Use Case |
|-------------|----------|
| `production` | Main branch deployments |
| `preview` | PR/branch previews |
| `development` | Local dev (`vercel dev`) |

### System Variables

| Variable | Description |
|----------|-------------|
| `VERCEL` | Always `1` on Vercel |
| `VERCEL_ENV` | `production`, `preview`, `development` |
| `VERCEL_URL` | Deployment URL (no protocol) |
| `VERCEL_REGION` | Region code (e.g., `iad1`) |
| `VERCEL_GIT_COMMIT_SHA` | Git commit SHA |

---

## Common Workflows

### 1. Project Setup
```bash
vercel link --yes --project myapp
vercel pull --yes --environment development
```

### 2. Deploy
```bash
vercel --yes                    # Preview
vercel --prod --yes             # Production
```

### 3. Staged Production
```bash
vercel --prod --skip-domain --yes > staged-url.txt
# Test the staged deployment
vercel promote $(cat staged-url.txt) --yes
```

### 4. Environment Variables
```bash
vercel env ls production
echo "secret" | vercel env add API_KEY production
vercel env rm OLD_KEY --yes
```

### 5. Debug Deployment
```bash
vercel logs <deployment-url>
vercel logs <url> --json | jq '.message'
vercel inspect <url>
```

### 6. Rollback
```bash
vercel rollback <deployment-url>
```

> Advanced workflows (CI/CD, blue-green, canary) in [REFERENCE.md](./REFERENCE.md#advanced-deployment-patterns)

---

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `command not found: vercel` | Not installed | `npm i -g vercel` |
| `Not authorized` | Invalid token | Check VERCEL_TOKEN |
| `Project not found` | Wrong name | `vercel project ls` |
| `No project linked` | Not linked | `vercel link --yes --project <name>` |
| `Domain already in use` | On other project | Use `--force` |
| `Deployment failed` | Build error | Check `vercel logs` |

### Quick Troubleshooting
```bash
vercel whoami                    # Verify auth
vercel --token $VERCEL_TOKEN whoami  # Check token
vercel logs <url>                # View errors
vercel inspect <url>             # Deployment details
```

> Deep troubleshooting in [REFERENCE.md](./REFERENCE.md#troubleshooting-deep-dive)

---

## Framework Examples

### Next.js
```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "framework": "nextjs",
  "regions": ["iad1", "sfo1"]
}
```

### React (Vite)
```json
{
  "framework": "vite",
  "buildCommand": "npm run build",
  "outputDirectory": "dist"
}
```

> More frameworks in [REFERENCE.md](./REFERENCE.md#framework-detection)

---

## Agent Integration

### Auto-Detection Triggers
- `vercel.json` or `.vercel` directory
- `VERCEL_TOKEN` in `.env`
- User mentions "Vercel", "deploy to Vercel"

### Pattern Recognition
```yaml
High-confidence:
  - "Deploy to Vercel"
  - "vercel deploy", "Vercel logs"
  - "Add domain to Vercel"

Medium-confidence:
  - "Deploy frontend"
  - "Next.js deployment"
```

### Handoff to Deep-Debugger
- Build failures with unclear errors
- Runtime errors in serverless functions
- Performance issues requiring profiling

Provide: `vercel logs` output, `vercel inspect` output, `vercel.json`

---

## Quick Reference Card

```bash
# Auth
export VERCEL_TOKEN="xxx"
vercel --token $VERCEL_TOKEN whoami

# Project
vercel link --yes --project myapp
vercel project ls
vercel project rm myapp --yes

# Deploy
vercel --yes                          # Preview
vercel --prod --yes                   # Production
vercel promote <url> --yes            # Promote

# Rollback
vercel rollback <url>

# Env Vars
vercel env ls production
echo "value" | vercel env add KEY production
vercel env rm KEY --yes
vercel pull --yes --environment production

# Domains
vercel domains ls
vercel domains add api.example.com myapp
vercel domains rm api.example.com --yes

# Debug
vercel logs <url>
vercel inspect <url>
vercel list --json
```

---

**See Also**: [REFERENCE.md](./REFERENCE.md) for CI/CD integration, multi-region config, security, cost optimization
