---
name: ln-751-command-templates
description: Generates individual .claude/commands files from templates
---

# ln-751-command-templates

**Type:** L3 Worker
**Category:** 7XX Project Bootstrap
**Parent:** ln-750-commands-generator

Generates Claude Code commands from templates with variable substitution.

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | Template name, variable values from ln-750 |
| **Output** | `.claude/commands/{command}.md` file |
| **Templates** | Located in `references/` directory |

---

## Available Templates

| Template | Output File | Required |
|----------|-------------|----------|
| `refresh_context_template.md` | refresh_context.md | Always |
| `refresh_infrastructure_template.md` | refresh_infrastructure.md | Always |
| `build_and_test_template.md` | build-and-test.md | Always |
| `ui_testing_template.md` | ui-testing.md | If Playwright |
| `deploy_template.md` | deploy.md | If CI/CD |
| `database_ops_template.md` | database-ops.md | If Database |

---

## Workflow

1. **Receive** template name and variables from ln-750
2. **Load** template from `references/{template}.md`
3. **Substitute** all `{{VARIABLE}}` placeholders
4. **Write** to `.claude/commands/` directory
5. **Report** success/failure to coordinator

---

## Variable Syntax

All templates use Handlebars-style syntax: `{{VARIABLE_NAME}}`

Common variables:
- `{{PROJECT_NAME}}` — Project name
- `{{FRONTEND_ROOT}}` — Frontend source path
- `{{BACKEND_ROOT}}` — Backend source path
- `{{FRONTEND_PORT}}` — Frontend dev server port
- `{{BACKEND_PORT}}` — Backend API port
- `{{TECH_STACK}}` — Technology stack summary

See individual templates in `references/` for full variable lists.

---

**Version:** 2.0.0
**Last Updated:** 2026-01-10
