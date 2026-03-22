---
name: workflow-e2e-update-ui
version: 1.0.0
description: '[Workflow] Trigger E2E Update UI workflow — update e2e screenshot baselines after ui changes.'
---

> **[IMPORTANT]** This skill activates a full workflow. You MUST create todo tasks for ALL steps and execute them in sequence. Do NOT skip any step.

Activate the `e2e-update-ui` workflow. Run `/workflow-start e2e-update-ui` with the user's prompt as context.

**Steps:** /scout → /e2e-test → /test → /watzup → /workflow-end
