---
version: 4.1.0-fractal
name: conductor-implement
description: Execute tasks from a track's implementation plan following TDD workflow
metadata:
  argument-hint: "[track-id] [--task X.Y] [--phase N]"
---

# Implement Track

Execute tasks from a track's implementation plan, following the workflow rules defined in `conductor/workflow.md`.

## Use this skill when

- Working on implement track tasks or workflows
- Needing guidance, best practices, or checklists for implement track

## Do not use this skill when

- The task is unrelated to implement track
- You need a different domain or tool outside this scope

## Instructions

- Clarify goals, constraints, and required inputs.
- Apply relevant best practices and validate outcomes.
- Provide actionable steps and verification.
- If detailed examples are required, open `resources/implementation-playbook.md`.

## Pre-flight Checks

1. Verify Conductor is initialized:
   - Check `conductor/product.md` exists
   - Check `conductor/workflow.md` exists
   - Check `conductor/tracks.md` exists
   - If missing: Display error and suggest running `/conductor:setup` first

2. Load workflow configuration:
   - Read `conductor/workflow.md`
   - Parse TDD strictness level
   - Parse commit strategy
   - Parse verification checkpoint rules

## Track Selection

## 🧠 Knowledge Modules (Fractal Skills)

### 1. [If argument provided:](./sub-skills/if-argument-provided.md)
### 2. [If no argument:](./sub-skills/if-no-argument.md)
### 3. [1. Task Identification](./sub-skills/1-task-identification.md)
### 4. [2. Task Start](./sub-skills/2-task-start.md)
### 5. [3. TDD Workflow (if TDD enabled in workflow.md)](./sub-skills/3-tdd-workflow-if-tdd-enabled-in-workflowmd.md)
### 6. [4. Non-TDD Workflow (if TDD not strict)](./sub-skills/4-non-tdd-workflow-if-tdd-not-strict.md)
### 7. [5. Task Completion](./sub-skills/5-task-completion.md)
### 8. [6. Phase Completion Check](./sub-skills/6-phase-completion-check.md)
### 9. [On Tool Failure](./sub-skills/on-tool-failure.md)
### 10. [On Test Failure](./sub-skills/on-test-failure.md)
### 11. [On Git Failure](./sub-skills/on-git-failure.md)
### 12. [1. Final Verification](./sub-skills/1-final-verification.md)
### 13. [2. Update Track Status](./sub-skills/2-update-track-status.md)
### 14. [3. Documentation Sync Offer](./sub-skills/3-documentation-sync-offer.md)
### 15. [4. Cleanup Offer](./sub-skills/4-cleanup-offer.md)
### 16. [5. Completion Summary](./sub-skills/5-completion-summary.md)
