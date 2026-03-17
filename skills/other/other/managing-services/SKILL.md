---
name: managing-services
description: |
  Manage Digital FTE services as supervised child processes.
  Use when starting all services, debugging service crashes,
  configuring auto-restart behavior, or checking service status.
  NOT when running individual watchers (use specific watcher skills).
---

# Service Manager Skill

Process supervisor for all Digital FTE services.

## Quick Start

```bash
# Start all services
python scripts/run.py
```

## Managed Services

1. Gmail Watcher
2. WhatsApp Watcher
3. Filesystem Watcher
4. Orchestrator

## Features

- Auto-restart on crash
- Graceful shutdown (Ctrl+C)
- Startup logging to `Vault/Logs/startup_log.md`
- Configurable restart delays

## Windows Task Scheduler

Install as startup task:
```powershell
.\scripts\install_service.ps1
```

## Verification

Run: `python scripts/verify.py`
