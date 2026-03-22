---
name: workflow-refactor
version: 1.0.0
description: '[Workflow] Trigger Code Refactoring workflow — restructure and improve existing code without changing behavior.'
---

> **[IMPORTANT]** This skill activates a full workflow. You MUST create todo tasks for ALL steps and execute them in sequence. Do NOT skip any step.

Activate the `refactor` workflow. Run `/workflow-start refactor` with the user's prompt as context.

**Steps:** /scout → /feature-investigation → /plan → /plan-review → /plan-validate → /why-review → /code → /tdd-spec → /tdd-spec-review → /test-specs-docs → /code-simplifier → /review-changes → /code-review → /sre-review → /changelog → /test → /docs-update → /watzup → /workflow-end
