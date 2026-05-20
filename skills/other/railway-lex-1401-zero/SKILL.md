---
name: Railway Tool
description: Deploy and manage services on Railway.app
---

# Railway Tool

Integrates with the `railway` CLI.

## Prerequisites

- Install Railway CLI: `npm i -g @railway/cli`
- Login: `railway login`

## Actions

### Init

Initialize a new project.

```bash
railway init
```

### Up (Deploy)

Deploy the current directory.

```bash
railway up
```

### Status

Show the status of the latest deployment.

```bash
railway status
```

### Logs

Tail logs for the current project.

```bash
railway logs
```
