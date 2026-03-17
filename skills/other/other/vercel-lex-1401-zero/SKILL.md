---
name: Vercel Tool
description: Implante projetos web e gerencie implantações na Vercel.
---

# Vercel Tool

Integrates with the `vercel` CLI to manage deployments.

## Prerequisites

- Install Vercel CLI: `npm i -g vercel`
- Login: `vercel login`

## Actions

### Deploy

Deploy the current directory to Vercel.

```bash
vercel deploy --prod
```

### List Projects

List your Vercel projects.

```bash
vercel project list
```

### Inspect Deployment

Inspect a deployment by URL or ID.

```bash
vercel inspect <url-or-id>
```
