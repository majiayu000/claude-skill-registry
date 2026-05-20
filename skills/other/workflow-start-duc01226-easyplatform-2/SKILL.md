---
name: workflow-start
version: 1.0.0
description: "[Skill Management] Activate a workflow from the injected catalog. Use when starting a detected workflow, initializing workflow state, or activating a workflow sequence. Triggers on "start workflow", "activate workflow", "workflow-start", "begin workflow"."
allowed-tools: TaskCreate
---

> **[MANDATORY]** You MUST use `TaskCreate` to break ALL work into small tasks BEFORE starting. NEVER skip task creation.

## Quick Summary

**Goal:** Activate a workflow by ID, creating tracking tasks and announcing the workflow sequence.

**Workflow:**
1. **Match** -- Validate workflow ID against catalog
2. **Create** -- Set up TaskCreate items for all workflow steps
3. **Announce** -- Tell user the detected intent and workflow sequence

**Key Rules:**
- MUST be called as first action after workflow detection (for non-trivial tasks)
- For simple tasks, AI MUST ask user whether to skip workflow
- Create workflow-level tasks BEFORE any implementation tasks

# Workflow Start

Activate a workflow from the injected catalog and initialize step tracking via TaskCreate.

---

## When to Use

- Starting a detected workflow from the injected catalog
- Initializing workflow state for step-by-step execution
- Switching from one active workflow to another

**NOT for**: Manual step execution (follow TaskCreate items), workflow design (use `planning`), or workflow catalog management.

---

## Quick Reference

### Workflow

1. Read the workflow catalog injected by the hook
2. Validate the workflow ID against available entries
3. Create workflow state via the workflow-step-tracker hook
4. Create TaskCreate items for ALL sequence steps immediately
5. Begin first step, marking it `in_progress`

### Related

- **Command:** `/workflow-start <workflowId>`
- **Hook:** `workflow-step-tracker.cjs`
- **Hook:** `workflow-router.cjs`

---

## Activation Rules

- Call ONLY after reading the workflow catalog injected by the hook
- Use the exact workflow ID shown in the catalog (e.g., `feature`, `bugfix`, `investigation`)
- If the workflow has **Confirm first** marker, ask the user BEFORE activation
- If called while another workflow is active, it will auto-switch (end current, start new)

---

## After Activation

Your FIRST action after activation MUST be calling `TaskCreate` once for EACH workflow step:

    TaskCreate: subject="[Workflow] /step-command - Step description", description="Workflow step", activeForm="Executing step"

Create ALL tasks first, then mark the first task `in_progress` via `TaskUpdate`. Do NOT skip this.

---

## See Also

- `planning` skill - Creating implementation plans
- `feature-implementation` skill - Implementing features after planning
- `debug` skill - Bug fix workflows

---

## IMPORTANT Task Planning Notes (MUST FOLLOW)

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
