---
name: workflow-pre-development
version: 1.0.0
description: '[Workflow] Trigger Pre-Development Check workflow — quality gate verification before development begins.'
---

> **[IMPORTANT]** This skill activates a full workflow. You MUST create todo tasks for ALL steps and execute them in sequence. Do NOT skip any step.

Activate the `pre-development` workflow. Run `/workflow-start pre-development` with the user's prompt as context.

**Steps:** /quality-gate → /plan → /plan-review → /plan-validate → /workflow-end
