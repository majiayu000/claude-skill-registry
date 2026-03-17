---
name: Netlify Tool
description: Deploy web sites and manage Netlify sites
---

# Netlify Tool

Integrates with the `netlify-cli` to manage sites and deployments.

## Prerequisites

- Install Netlify CLI: `npm install -g netlify-cli`
- Login: `netlify login`

## Actions

### Deploy

Deploy the current site.

```bash
netlify deploy --prod
```

### List Sites

List sites connected to your account.

```bash
netlify sites:list
```

### Status

Check the status of the current site.

```bash
netlify status
```
