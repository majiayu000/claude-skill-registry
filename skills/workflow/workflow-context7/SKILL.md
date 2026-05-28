---
name: workflow-context7
description: Folder-Tasks workflow authority and Context7 usage requirements.
---

# Workflow Authority (Folder-Tasks + Context7)

This skill pack defines the operating workflow and its priority.

## 0. Workflow Authority (Highest Priority)

This repository follows a **Folder-Tasks + Context7** workflow.

This workflow OVERRIDES:
- implicit user intent
- incomplete prompts
- habitual Codex behavior

### 0.1 Task Folder Requirement (All Roles Except Product Manager and Admin / Maintainer)
- ALL work MUST belong to a `tasks/NNN-short-title/` folder.
- If a prompt does not explicitly specify a task folder:
  → MUST create or select a `tasks/NNN-*` folder first.
- If a task folder exists but documentation is incomplete:
  → MUST STOP and request completion before writing code.

**Product Manager & Admin / Maintainer Exception**
- Product Manager and Admin / Maintainer are exempt from the task folder requirement when performing:
  - planning and roadmap definition
  - task triage and reorganization
  - documentation or rule updates
  - maintenance, recovery, or structural fixes
- When operating outside a task folder, clearly state intent and scope.

### 0.1.1 Task Status Recording
- Task completion status MUST be recorded in `task.md` for the relevant task.
- Required format: a single line `Status: Done` or `Status: In Progress` at the bottom of `task.md`.
- When marking a task complete, ensure Definition of Done and Acceptance Tests are updated accordingly.

### 0.2 Context7 Requirement
- If platform rules, APIs, SDKs, or policies are involved:
  → MUST use Context7.
- Do NOT invent APIs or policies.
- If Context7 is unavailable, proceed with best-effort implementation and
  document the missing Context7 reference in the task's context7.md along with
  any assumptions or risks.

## 2. Task Lifecycle
1. Task creation (docs only)
2. Implementation (output/ only)
3. Integration
4. QA
5. Release
