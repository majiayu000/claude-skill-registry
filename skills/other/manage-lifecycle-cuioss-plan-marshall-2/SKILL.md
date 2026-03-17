---
name: manage-lifecycle
description: Plan lifecycle operations - discovery, phase transitions, archiving, and routing
user-invocable: false
allowed-tools: Read, Glob, Bash
---

# Manage Lifecycle Skill

Plan lifecycle operations including discovery, phase transitions, archiving, and routing context.

## Script API

Script: `pm-workflow:manage-lifecycle:manage-lifecycle`

| Command | Parameters | Description |
|---------|------------|-------------|
| `list` | `[--filter]` | Discover all plans |
| `transition` | `--plan-id --completed` | Transition to next phase |
| `archive` | `--plan-id [--dry-run]` | Archive completed plan |
| `route` | `--phase` | Get skill for phase |
| `get-routing-context` | `--plan-id` | Get combined routing context |
