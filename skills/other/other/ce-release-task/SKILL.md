---
name: ce-release-task
description: >
  Identify the next release task from RELEASE_PLAN_v1.md and vX.Y.Z_plan.md,
  plan implementation, execute it, and verify closure with tests and gates.
---

# CE Release Task

You are identifying, implementing, and verifying a single release task from the
current version plan.

## Required references

- `docs/improvement/RELEASE_PLAN_v1.md` (master plan and ADR gap appendix)
- `docs/improvement/vX.Y.Z_plan.md` (current version implementation plan)
- Governing ADRs and standards for the selected task
- `CONTRIBUTOR_INSTRUCTIONS.md` (coding and testing rules)

## Use this skill when

- Picking the next actionable task from the current release plan.
- Implementing a specific release task end-to-end.
- Verifying that a release task is firmly closed.

## Workflow

### Phase 1: Task Selection

1. Read `RELEASE_PLAN_v1.md` current version section and `vX.Y.Z_plan.md`.
2. Identify tasks by status:
   - **Completed**: has verification evidence (tests green, code merged).
   - **In progress**: partially implemented.
   - **Not started**: no implementation yet.
3. Select the highest-priority not-started or in-progress task, considering:
   - dependency ordering (blocked vs. unblocked)
   - ADR gap severity from the appendix
   - user preference (if specified)

### Phase 2: Planning

4. Read the task section in `vX.Y.Z_plan.md` for implementation steps.
5. Read all governing ADRs, standards, and source files referenced.
6. Identify the specific code changes needed:
   - which files to modify or create
   - which tests to add
   - which documentation to update
7. Consult `ce-adr-consult` if the task touches ADR-governed behavior.
8. Present the implementation plan to the user for approval.

### Phase 3: Implementation

9. Implement the code changes following CE coding standards.
10. Write tests per the `ce-test-author` rubric.
11. Run `make local-checks-pr` to validate.
12. If tests fail, diagnose and fix before proceeding.

### Phase 4: Verification

13. Run the task-specific verification checklist from `vX.Y.Z_plan.md`.
14. Confirm:
    - all new tests pass
    - no coverage regression
    - no existing test breakage
    - ADR gap status can be updated (severity -> 0 if fully closed)
15. Update the task status in `vX.Y.Z_plan.md` with a completion date and
    brief status note.

## Output contract

For each completed task, provide:
- summary of changes made
- files modified
- tests added/modified
- verification evidence (test output, coverage)
- updated status in `vX.Y.Z_plan.md`

## Constraints

- One task at a time. Do not batch unrelated tasks.
- Always run verification before declaring a task closed.
- Do not update `RELEASE_PLAN_v1.md` appendix scores without evidence.
- Follow CE-first coding rules: use `WrapCalibratedExplainer` and
  `ce_agent_utils` helpers, not ad-hoc wrappers.
