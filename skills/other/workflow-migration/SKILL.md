---
name: workflow-migration
version: 1.0.0
description: '[Workflow] Trigger Database Migration workflow — schema changes, data migrations, EF migrations with review and testing.'
---

> **[IMPORTANT]** This skill activates a full workflow. You MUST create todo tasks for ALL steps and execute them in sequence. Do NOT skip any step.

Activate the `migration` workflow. Run `/workflow-start migration` with the user's prompt as context.

**Steps:** /scout → /feature-investigation → /plan → /plan-review → /plan-validate → /code → /review-changes → /code-review → /sre-review → /test → /docs-update → /watzup → /workflow-end
