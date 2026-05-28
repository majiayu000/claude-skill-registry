---
name: ln-751-command-templates
description: Generates individual .claude/commands files from templates
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

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

**MANDATORY READ:** Load templates from `references/` for full variable lists.

---

## Critical Rules

- **Template-driven only:** All output generated from `references/` templates, never freeform
- **Full substitution:** Every `{{VARIABLE}}` must be replaced; fail if any placeholder unresolved
- **Write to correct path:** Output always goes to `.claude/commands/`, never elsewhere
- **No template modification:** Templates in `references/` are read-only; only output files are written

## Definition of Done

- Template loaded from `references/{template}.md`
- All `{{VARIABLE}}` placeholders substituted with values from ln-750
- Output written to `.claude/commands/{command}.md`
- Success/failure reported back to coordinator

## Reference Files

- **refresh_context_template.md:** [references/refresh_context_template.md](references/refresh_context_template.md)
- **refresh_infrastructure_template.md:** [references/refresh_infrastructure_template.md](references/refresh_infrastructure_template.md)
- **build_and_test_template.md:** [references/build_and_test_template.md](references/build_and_test_template.md)
- **ui_testing_template.md:** [references/ui_testing_template.md](references/ui_testing_template.md)
- **deploy_template.md:** [references/deploy_template.md](references/deploy_template.md)
- **database_ops_template.md:** [references/database_ops_template.md](references/database_ops_template.md)

---

**Version:** 2.0.0
**Last Updated:** 2026-01-10
