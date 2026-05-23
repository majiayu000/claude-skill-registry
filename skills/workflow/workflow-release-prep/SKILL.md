---
name: workflow-release-prep
version: 1.0.0
description: '[Workflow] Trigger Release Preparation workflow — pre-release quality gate with sre review and status verification.'
---

> **[IMPORTANT]** This skill activates a full workflow. You MUST create todo tasks for ALL steps and execute them in sequence. Do NOT skip any step.

Activate the `release-prep` workflow. Run `/workflow-start release-prep` with the user's prompt as context.

**Steps:** /sre-review → /quality-gate → /status → /workflow-end
