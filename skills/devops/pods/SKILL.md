---
name: pods
description: |
  Aggregate management for all AI pod services. Provides status overview
  and bulk operations across all pod containers (ollama, jupyter, comfyui,
  openwebui, localai, fiftyone, jellyfin, runners).
---

# Pods - Aggregate Pod Management

## Overview

The `pods` command provides aggregate management for all AI pod services. It shows combined status and enables bulk operations across all running pod containers.

**Key Concept:** This is a meta-command for managing multiple pods at once. For individual pod management, use the specific service command (e.g., `ujust ollama`, `ujust jupyter`).

## Quick Reference

| Action | Command | Description |
|--------|---------|-------------|
| Status | `ujust pods status` | Show status of all pods |
| Purge | `ujust pods purge` | Remove all pod containers |

## Parameters

### ACTION Parameter

```bash
ujust pods ACTION=""
```

| Parameter | Values | Description |
|-----------|--------|-------------|
| `ACTION` | `status`, `purge` | Action to perform |

Without `ACTION`, shows interactive menu (requires TTY).

## Commands

### Status

```bash
ujust pods status
```

Shows status of all pod services:

- Container running state
- Port bindings
- GPU attachment
- Resource usage

**Output includes:**

- Ollama
- Jupyter
- ComfyUI
- Open WebUI
- LocalAI
- FiftyOne
- Jellyfin
- GitHub Runners

### Purge

```bash
ujust pods purge
```

Removes all pod containers and their configurations:

1. Stops all running pods
2. Removes all pod containers
3. Cleans up Quadlet configs
4. Reloads systemd

**Warning:** This removes ALL pod containers. Data in workspace directories is preserved.

## Common Workflows

### Check All Services

```bash
# Quick status overview
ujust pods status
```

### Clean Restart

```bash
# Remove all pods
ujust pods purge

# Reconfigure and start individual services
ujust ollama config
ujust ollama start
```

### Before System Update

```bash
# Check what's running
ujust pods status

# Stop all if needed
ujust pods purge
```

## Non-Interactive Usage

All commands work without TTY:

```bash
# CI/automation-friendly
ujust pods status
ujust pods purge
```

## Troubleshooting

### Status Shows Stale Containers

**Symptom:** Status shows containers that don't exist

**Cause:** Quadlet configs out of sync

**Fix:**

```bash
systemctl --user daemon-reload
ujust pods status
```

### Purge Doesn't Remove All

**Symptom:** Some containers remain after purge

**Cause:** Containers created outside Quadlet

**Fix:**

```bash
# Manual cleanup
podman ps -a
podman rm -f <container-id>
```

## Cross-References

- **Individual Services:** `ollama`, `jupyter`, `comfyui`, `openwebui`, `localai`, `fiftyone`, `jellyfin`, `runners` skills
- **Testing:** `test pods` for lifecycle testing

## When to Use This Skill

Use when the user asks about:

- "all pods status", "check all services"
- "remove all containers", "clean up pods"
- "what's running", "show all services"
- "purge containers", "reset pods"
