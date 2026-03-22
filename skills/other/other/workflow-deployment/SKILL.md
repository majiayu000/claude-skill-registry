---
name: workflow-deployment
version: 1.0.0
description: '[Workflow] Trigger Deployment & Infrastructure workflow — CI/CD pipelines, Docker, Kubernetes setup and deployment.'
---

> **[IMPORTANT]** This skill activates a full workflow. You MUST create todo tasks for ALL steps and execute them in sequence. Do NOT skip any step.

Activate the `deployment` workflow. Run `/workflow-start deployment` with the user's prompt as context.

**Steps:** /scout → /feature-investigation → /plan → /plan-review → /plan-validate → /code → /review-changes → /code-review → /sre-review → /test → /watzup → /workflow-end
