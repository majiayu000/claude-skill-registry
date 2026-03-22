---
name: workflow-design-dev-handoff
version: 1.0.0
description: '[Workflow] Trigger Designer to Dev Handoff workflow — designer hands off design spec to developer for implementation.'
---

> **[IMPORTANT]** This skill activates a full workflow. You MUST create todo tasks for ALL steps and execute them in sequence. Do NOT skip any step.

Activate the `design-dev-handoff` workflow. Run `/workflow-start design-dev-handoff` with the user's prompt as context.

**Steps:** /design-spec → /review-artifact → /handoff → /plan → /plan-review → /plan-validate → /workflow-end
