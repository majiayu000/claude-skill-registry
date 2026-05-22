---
name: vercel-workflow-builder
description: Vercel deployment workflow builder and CI/CD
allowed-tools: [Bash, Read, WebFetch]
---

# Vercel Workflow Builder Skill

## Overview

Vercel deployment workflows and CI/CD. 90%+ context savings.

## Requirements

- VERCEL_TOKEN environment variable
- Vercel CLI installed

## Tools (Progressive Disclosure)

### Deployments

| Tool     | Description               | Confirmation |
| -------- | ------------------------- | ------------ |
| deploy   | Deploy to Vercel          | Yes          |
| preview  | Create preview deployment | No           |
| promote  | Promote to production     | Yes          |
| rollback | Rollback deployment       | Yes          |

### Projects

| Tool             | Description         |
| ---------------- | ------------------- |
| list-projects    | List projects       |
| project-info     | Get project details |
| list-deployments | List deployments    |

### Environment

| Tool       | Description         | Confirmation |
| ---------- | ------------------- | ------------ |
| env-list   | List env variables  | No           |
| env-add    | Add env variable    | Yes          |
| env-remove | Remove env variable | Yes          |

## Agent Integration

- **devops** (primary): CI/CD setup
- **developer** (secondary): Deployment workflows
