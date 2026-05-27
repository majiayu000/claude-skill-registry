---
name: complete-implementation
description:"\"Holistic completion workflow after a feature's tasks are marked COMPLETE: code review, feature verification, integration check, documentation drift audit/update, and context refinement. Creates follow-up task files when issues are found.\""
version: "1.0.0"
last_updated: "2026-01-27"
python_compatibility: "3.11+"
user-invocable: true
argument-hint: "<task-file-path>"
---

# Complete Implementation (Quality Gates + Recursion)

You MUST validate that the implemented feature meets its goals and quality gates. This workflow is recursive: if follow-up task files are created, re-run `implement-feature` on them and then re-run this skill.

<task_file>
$ARGUMENTS
</task_file>

---

## Phase 1: Code Review

Launch `code-reviewer` with the task file path.

---

## Phase 2: Feature Verification (goal-backward)

Launch `feature-verifier` with the task file path.

---

## Phase 3: Integration Check

Launch `integration-checker` with the task file path.

---

## Phase 4: Documentation Drift Audit

Launch `doc-drift-auditor` with the task file path (audit-only).

---

## Phase 5: Documentation Update (if drift found)

If drift exists or docs must be updated for the feature, launch `service-documentation`.

---

## Phase 6: Context Refinement

Launch `context-refinement` to update the task file Context Manifest with discoveries from implementation (only if needed).

---

## Recursive Follow-up Handling

If Phase 1 creates follow-up task files (expected naming: `plan/tasks-{N}-{slug}-followup-{k}.md`), run:

```text
Skill(skill="implement-feature", args="{followup_task_file_path}")
```

Then re-run `complete-implementation` on the follow-up task file.
