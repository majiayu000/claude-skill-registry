---
name: render
description: Render unified cloud for web services. Use for managed hosting.
---

# Render

Render is a unified cloud platform. It competes with Heroku and AWS. 2025 features: **Blueprints** (Infrastructure as Code) and **Preview Environments**.

## When to Use

- **All-in-One**: Host Static Sites, Web Services, Workers, Cron Jobs, and Redis/Postgres in one UI.
- **Cost Prediction**: Flat pricing (e.g. $7/mo) means no surprise AWS bills.
- **Auto-Scale**: One-checkbox auto-scaling based on CPU/RAM.

## Quick Start

```yaml
# render.yaml (Blueprint)
services:
  - type: web
    name: my-api
    env: node
    plan: starter
    buildCommand: npm install && npm run build
    startCommand: npm start
    envVars:
      - key: PORT
        value: 10000
    autoDeploy: true
```

## Core Concepts

### Blueprints

Define your entire stack in `render.yaml`. Syncs with Git.

### Private Services

Internal microservices that are not exposed to the internet, only to other services in your account.

### Disks

Unlike Heroku/Railway, Render supports **Persistent Disks**. You can attach a 10GB drive to a service (great for CMS uploads or SQLite).

## Best Practices (2025)

**Do**:

- **Use Blueprints**: Don't click around the UI. Version control your infrastructure.
- **Use Persistent Disks**: Enable stateful workloads (like standard WordPress or custom databases).
- **Use DDoS Protection**: Built-in cloudflare integration protects your apps.

**Don't**:

- **Don't mix regions**: Services in Oregon cannot talk to Private Services in Frankfurt via internal releases. Keep stack in one region.

## References

- [Render Documentation](https://render.com/docs)
