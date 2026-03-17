---
name: mpm
description: Access Claude MPM functionality and manage multi-agent orchestration
user-invocable: true
version: "1.0.0"
category: mpm-command
tags: [mpm-command, system, pm-required]
---

# /mpm

Access Claude MPM functionality and manage your multi-agent orchestration.

## Available MPM Commands

- `/mpm-agents` - Show available agents and versions
- `/mpm-doctor` - Run diagnostic checks
- `/mpm-help` - Show command help
- `/mpm-status` - Show MPM status
- `/mpm-ticket` - Ticketing workflow management (organize, proceed, status, update, project)
- `/mpm-config` - Manage configuration
- `/mpm-resume` - Create session resume files
- `/mpm-version` - Display version information for project, agents, and skills

## What is Claude MPM?

Claude MPM extends Claude Code with:
- **Multi-agent orchestration** - Delegate work to specialized agents
- **Project-specific PM instructions** - Tailored guidance for your project
- **Agent memory management** - Context-aware agent interactions
- **WebSocket monitoring** - Real-time system monitoring
- **Hook system for automation** - Automate workflows and tasks

## Quick Start

Use `/mpm-help` to explore commands or `/mpm-status` to check system health.

For more information, use `/mpm-help [command]` for specific command details.
