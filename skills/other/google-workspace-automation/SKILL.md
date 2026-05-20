---
name: google-workspace-automation
description: Design Gmail, Drive, Sheets, and Calendar automations with scope-aware plans. Use for repeatable daily task automation with explicit OAuth scopes and audit-ready outputs.
---

# Google Workspace Automation

## Overview

Create structured automation plans for common Gmail, Drive, Sheets, and Calendar workflows.

## Workflow

1. Define automation goal, services, and actions.
2. Derive required OAuth scopes and integration boundaries.
3. Build execution plan with schedule and retry behavior.
4. Export auditable artifact for implementation.

## Use Bundled Resources

- Run `scripts/plan_workspace_automation.py` for deterministic automation planning.
- Read `references/workspace-guide.md` for scope and quota considerations.

## Guardrails

- Always declare least-privilege scopes.
- Keep automations idempotent and auditable.
