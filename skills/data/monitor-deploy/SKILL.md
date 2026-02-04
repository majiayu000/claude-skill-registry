---
name: monitoring-deployments
description: Use this skill when monitoring Spotify deployments, checking deployment status, viewing deploy progress, or tailing deployment logs. Triggers on "check deployment", "deploy status", "monitor deploy", "what's deploying", or when user runs /monitor-deploy.
---

# Monitoring Deployments

Monitor Spotify deployments via the Tugboat CLI with optional GCP log tailing.

## Prerequisites

Check if `tugboat` exists. If not, auto-install:

```bash
uv tool install --from git+ssh://git@ghe.spotify.net/warpspeed/tugboat-cli.git tugboat-cli
```

## Workflow

### 1. Get component

Use provided component name/pattern, or ask the user.

### 2. List installations

```bash
tugboat installations list --component=<component-or-pattern>
```

### 3. Get deployment status

```bash
tugboat deployments show --installation=<installation-id> <deployment-id>
```

For full JSON details:

```bash
tugboat deployments dump --installation=<installation-id> <deployment-id>
```

### 4. Get version info

```bash
tugboat version <component-id> show <version-id>
```

### 5. Summarize

Present concisely: state, progress %, version/commit, errors.

### 6. Offer log tailing

When in-progress or failed, offer to tail GCP logs. Parse log info from tugboat output and run:

```bash
gcloud logging tail "<filter>" --project=<project>
```

## Batch mode

For patterns like `fan-audio-*`, show a table of all matching components.

## Errors

- Auth issues → `gcloud auth login`
- Missing tugboat → auto-install
- Bad component → list available ones
