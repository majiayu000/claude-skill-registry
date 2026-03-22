---
name: workflow-review-changes
version: 1.0.0
description: '[Workflow] Trigger Review Current Changes workflow — review uncommitted changes before commit with summary report.'
---

> **[IMPORTANT]** This skill activates a full workflow. You MUST create todo tasks for ALL steps and execute them in sequence. Do NOT skip any step.

Activate the `review-changes` workflow. Run `/workflow-start review-changes` with the user's prompt as context.

**Steps:** /review-changes → /code-review → /watzup → /workflow-end
