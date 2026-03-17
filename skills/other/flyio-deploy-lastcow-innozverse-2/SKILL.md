---
name: innozverse-flyio-deploy
description: Deploy the innozverse API to Fly.io, manage deployments, check status, view logs, and troubleshoot deployment issues. Use when deploying the API or debugging Fly.io deployment problems.
---

# innozverse Fly.io Deployment Skill

Quick reference for deploying the innozverse API to Fly.io.

## Prerequisites

```bash
brew install flyctl  # macOS
fly auth login
```

## First Deployment

```bash
cd apps/api
fly launch  # Follow prompts
fly secrets set API_VERSION=1.0.0
fly deploy
```

## Subsequent Deployments

```bash
cd apps/api
fly deploy
```

## Common Commands

```bash
fly status              # Check app status
fly logs                # View logs
fly ssh console         # SSH into machine
fly secrets set KEY=val # Set environment variable
fly scale memory 512    # Scale memory
fly open                # Open app in browser
```

## Configuration (fly.toml)

Located at `apps/api/fly.toml`:
- `app`: App name on Fly.io
- `internal_port`: 8080 (must match PORT in code)
- `auto_stop_machines`: Scale to zero when idle
- Health check: `/health` endpoint

## Troubleshooting

**Build fails**: Check Dockerfile, verify dependencies
**Health check fails**: Test `/health` endpoint locally
**Connection issues**: Check `fly status`, verify region

## Resources

See [docs/deployment-flyio.md](../../docs/deployment-flyio.md) for full guide.
