---
name: vps-docker
description: Full VPS Docker status — all containers, resource usage, arifOS health
user-invocable: true
---

# VPS Docker Manager

When the user asks about containers, docker status, VPS health, or what's running:

1. Run `docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"` to list all containers
2. Run `docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"` for resource usage
3. Run `curl -s http://arifosmcp_server:8080/health | jq '{status,tools_loaded,version}'` for arifOS health
4. Show disk: `df -h /`

Present as a clean status table. Flag any containers not in `healthy` or `Up` state.

Trigger patterns: "docker status", "containers", "what's running", "vps status", "system health", "container status"
