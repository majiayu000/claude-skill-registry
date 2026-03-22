---
name: vercel
description: Monitor and manage Vercel deployments.
user-invocable: true
argument-hint: "<status|deploy|logs|rollback> [project-path]"
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
model: sonnet
---

# Vercel Deployment Manager

## Project Resolution

Determine the project path using this priority:
1. Path provided as argument (e.g., `/vercel status ~/my-project`)
2. Current project channel's configured path
3. Ask the user which project to check

All `vercel` commands below use `--cwd <project-path>`.

## Commands

### `status` — Show recent deployments
```bash
vercel list --cwd <project-path>
```
Report the current production URL, latest deployment status, and any recent failures.

### `deploy` — Deploy to production
**REQUIRES USER CONFIRMATION before executing.**
```bash
vercel --prod --cwd <project-path>
```
Show the user what will be deployed (current git status, branch, recent commits) and ask for explicit confirmation before running.

### `logs <url>` — View deployment logs
```bash
vercel logs <deployment-url> --cwd <project-path>
```
If no URL provided, get the latest deployment URL from `vercel list` first.

### `rollback` — Rollback to previous deployment
**REQUIRES USER CONFIRMATION before executing.**
```bash
vercel rollback --cwd <project-path>
```
Show the current and previous deployment before asking for confirmation.

## Notes

- Deploy and rollback are destructive operations — always confirm first
- The deploy-monitor heartbeat task checks deployment status every 30 minutes
- Project paths can be configured in `heartbeat-tasks/projects.json`
