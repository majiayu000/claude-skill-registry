---
name: agentic-devops
version: 1.0.1
description: Production-grade agent DevOps toolkit — Docker, process management, log analysis, and health monitoring. Built by engineers who run production.
author: Anvil AI
license: MIT
homepage: https://github.com/cacheforge-ai/cacheforge-skills
user-invocable: true
tags:
  - cacheforge
  - devops
  - docker
  - monitoring
  - log-analysis
  - health-check
  - infrastructure
  - sre
  - discord
  - discord-v2
metadata: {"openclaw":{"emoji":"🛠️","homepage":"https://github.com/cacheforge-ai/cacheforge-skills","requires":{"bins":["python3"]}}}
---

## When to use this skill

Use this skill when the user wants to:
- Run system diagnostics or health checks
- Manage Docker containers (status, logs, health, compose)
- Inspect running processes, ports, or resource hogs
- Analyze log files for errors, patterns, or frequency
- Check HTTP endpoint availability or port status
- Get a quick one-command system overview

## Commands

### Quick Diagnostics (start here)

```bash
# Full system health report — CPU, memory, disk, Docker, ports, errors, top processes
python3 skills/agentic-devops/devops.py diag
```

### Docker Operations

```bash
# Container status overview
python3 skills/agentic-devops/devops.py docker status

# Tail container logs with pattern filtering
python3 skills/agentic-devops/devops.py docker logs <container> --tail 100 --grep "error|warn"

# Docker health summary (running, stopped, unhealthy)
python3 skills/agentic-devops/devops.py docker health

# Docker Compose service status
python3 skills/agentic-devops/devops.py docker compose-status --file docker-compose.yml
```

### Process Management

```bash
# List processes sorted by resource usage
python3 skills/agentic-devops/devops.py proc list --sort cpu

# Show ports in use
python3 skills/agentic-devops/devops.py proc ports

# Detect zombie processes
python3 skills/agentic-devops/devops.py proc zombies
```

### Log Analysis

```bash
# Analyze log file for error patterns
python3 skills/agentic-devops/devops.py logs analyze /var/log/syslog --pattern "error|fail|critical"

# Tail log file with highlighted patterns
python3 skills/agentic-devops/devops.py logs tail /var/log/app.log --highlight "ERROR|WARN"

# Frequency analysis of log patterns
python3 skills/agentic-devops/devops.py logs frequency /var/log/app.log --top 20
```

### Health Checks

```bash
# Check HTTP endpoint health
python3 skills/agentic-devops/devops.py health check https://myapp.com/healthz

# Scan specific ports
python3 skills/agentic-devops/devops.py health ports 80,443,8080,5432

# System resource health (CPU, memory, disk)
python3 skills/agentic-devops/devops.py health system
```

## Requirements

- Python 3.8+ (stdlib only, no external dependencies)
- Docker CLI (optional — Docker sections degrade gracefully if not installed)
- Standard Unix utilities (ps, ss/netstat)
