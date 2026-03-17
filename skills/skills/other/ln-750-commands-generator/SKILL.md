---
name: ln-750-commands-generator
description: Generates project-specific .claude/commands for Claude Code
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

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
| `{{PROJECT_NAME}}` | package.json / .csproj | "my-app" |
| `{{TECH_STACK}}` | Auto-detected | "React + .NET + PostgreSQL" |
| `{{FRONTEND_ROOT}}` | Directory scan | "src/frontend" |
| `{{BACKEND_ROOT}}` | Directory scan | "src/MyApp.Api" |
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

## Critical Rules

- **Detect before generate:** Only create commands for detected stack components (no empty templates)
- **Variable completeness:** All `{{VARIABLE}}` placeholders must be resolved before delegation
- **Delegate via Task:** All template rendering goes through ln-751 with context isolation
- **No hardcoded paths:** All paths derived from project structure analysis, not assumptions

## Definition of Done

- Project structure analyzed and tech stack detected
- Variables extracted (project name, ports, roots, stack)
- Commands delegated to ln-751 with correct template name and variables
- All generated `.claude/commands/*.md` files verified to exist
- No unresolved `{{VARIABLE}}` placeholders remain in output

## Reference Files

- **Variables reference:** [references/variables_reference.md](references/variables_reference.md)
- **Questions:** [references/questions_commands.md](references/questions_commands.md)

---

**Version:** 2.0.0
**Last Updated:** 2026-01-10
