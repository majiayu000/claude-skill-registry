---
name: workflow-dev-qa-handoff
version: 1.0.0
description: '[Workflow] Trigger Dev to QA Handoff workflow — development complete, handoff to qa for testing.'
---

> **[IMPORTANT]** This skill activates a full workflow. You MUST create todo tasks for ALL steps and execute them in sequence. Do NOT skip any step.

Activate the `dev-qa-handoff` workflow. Run `/workflow-start dev-qa-handoff` with the user's prompt as context.

**Steps:** /handoff → /test-spec → /workflow-end
