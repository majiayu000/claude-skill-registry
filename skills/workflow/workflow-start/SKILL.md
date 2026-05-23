---
name: workflow-start
description: Activate a workflow from the injected catalog. Use when the workflow-router hook injects a catalog and a matching workflow is identified, or when the user explicitly requests a workflow activation (e.g., "start feature workflow", "activate bugfix workflow").
infer: true
allowed-tools: Skill, TodoWrite, AskUserQuestion, Read, Glob, Grep
---

# Workflow Activation

Start a workflow by ID from the workflow catalog injected by the hook system. This creates workflow state and prepares the step sequence for execution.

## When to Use

- After the workflow-router hook injects a catalog and you identify a matching workflow
- When the user explicitly asks to follow a specific workflow
- When switching from one active workflow to another

## Workflow

1. **Validate** the workflow ID against the injected catalog
2. **Confirm if needed** — If the workflow has a **Confirm first** marker, ask the user BEFORE activation
3. **Activate** — Invoke `/workflow:start <workflowId>` slash command to create workflow state via the workflow-step-tracker hook
4. **Create TodoWrite items** for ALL sequence steps immediately after activation
5. **Follow the sequence** in order, marking each step `in_progress` then `completed`

## Activation Rules

- Call this ONLY after reading the workflow catalog injected by the hook
- Use the exact workflow ID shown in the catalog (e.g., `feature`, `bugfix`, `investigation`)
- If the workflow has **Confirm first** marker, ask the user BEFORE calling this command
- If called while another workflow is active, it will auto-switch (end current, start new)

## After Activation

Your FIRST action after activation completes MUST be `TodoWrite` with items like:

    [Workflow] /step-command - Step description (status: in_progress for first, pending for rest)

Do NOT skip TodoWrite. It is a hard-blocking requirement.

## IMPORTANT Task Planning Notes (MUST FOLLOW)

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
