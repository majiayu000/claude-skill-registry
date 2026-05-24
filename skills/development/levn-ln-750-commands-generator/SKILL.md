---
name: ln-750-commands-generator
description: Generates project-specific .claude/commands for Claude Code
---

# ln-750-commands-generator

**Type:** L2 Domain Coordinator
**Category:** 7XX Project Bootstrap
**Parent:** ln-700-project-bootstrap

Generates `.claude/commands/` with project-specific Claude Code commands.

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | Project structure, tech stack |
| **Output** | .claude/commands/*.md files |
| **Worker** | ln-751-command-templates |

---

## Workflow

1. **Analyze** project structure and detect tech stack
2. **Extract** variables (paths, ports, frameworks)
3. **Delegate** to ln-751 with template name and variables
4. **Verify** generated commands exist

---

## Generated Commands

| Command | Purpose | Condition |
|---------|---------|-----------|
| refresh_context.md | Restore project context | Always |
| refresh_infrastructure.md | Restart services | Always |
| build-and-test.md | Full verification | Always |
| ui-testing.md | UI tests with Playwright | If Playwright detected |
| deploy.md | Deployment workflow | If CI/CD config exists |
| database-ops.md | Database operations | If database detected |

---

## Variables Extracted

| Variable | Source | Example |
|----------|--------|---------|
| `{{PROJECT_NAME}}` | package.json / .csproj | "kehai-os" |
| `{{TECH_STACK}}` | Auto-detected | "React + .NET + PostgreSQL" |
| `{{FRONTEND_ROOT}}` | Directory scan | "src/frontend" |
| `{{BACKEND_ROOT}}` | Directory scan | "src/Kehai.Api" |
| `{{FRONTEND_PORT}}` | vite.config / package.json | "3000" |
| `{{BACKEND_PORT}}` | launchSettings.json | "5000" |

Templates and full variable list: see `ln-751-command-templates/references/`

---

## Detection Logic

**Frontend:** vite.config.ts, package.json (react/vue/angular)
**Backend:** *.csproj with Web SDK, or express/fastapi in deps
**Database:** docker-compose.yml postgres/mysql, or connection strings
**Playwright:** playwright.config.ts or @playwright/test in deps
**CI/CD:** .github/workflows/, azure-pipelines.yml, Dockerfile

---

**Version:** 2.0.0
**Last Updated:** 2026-01-10
