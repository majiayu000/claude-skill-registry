---
name: workflow-qa-po-acceptance
version: 1.0.0
description: '[Workflow] Trigger QA to PO Acceptance workflow — testing complete, qa hands off to po for acceptance and sign-off.'
---

> **[IMPORTANT]** This skill activates a full workflow. You MUST create todo tasks for ALL steps and execute them in sequence. Do NOT skip any step.

Activate the `qa-po-acceptance` workflow. Run `/workflow-start qa-po-acceptance` with the user's prompt as context.

**Steps:** /quality-gate → /handoff → /acceptance → /workflow-end
