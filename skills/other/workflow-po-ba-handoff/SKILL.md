---
name: workflow-po-ba-handoff
version: 1.0.0
description: '[Workflow] Trigger PO to BA Handoff workflow — po hands off idea/pbi to ba for refinement and story creation.'
---

> **[IMPORTANT]** This skill activates a full workflow. You MUST create todo tasks for ALL steps and execute them in sequence. Do NOT skip any step.

Activate the `po-ba-handoff` workflow. Run `/workflow-start po-ba-handoff` with the user's prompt as context.

**Steps:** /idea → /review-artifact → /handoff → /refine → /refine-review → /story → /story-review → /pbi-challenge → /dor-gate → /workflow-end
