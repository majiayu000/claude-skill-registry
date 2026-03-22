---
name: ce-release-planner
description: >
  Analyze RELEASE_PLAN_v1.md for an upcoming release version and produce a
  detailed vX.Y.Z_plan.md implementation plan with task breakdowns.
---

# CE Release Planner

You are creating a versioned implementation plan for an upcoming CE release.

## Required references

- `docs/improvement/RELEASE_PLAN_v1.md` (master release plan with milestones,
  ADR gap appendix, and release gates)
- `references/version_plan_reference.md` (canonical structure/template for
  `docs/improvement/vX.Y.Z_plan.md` files)
- All ADR files referenced by the target milestone
- All STD files referenced by the target milestone
- Existing version plans for pattern reference:
  `docs/improvement/v0.11.0_plan.md`, `docs/improvement/v0.11.1_plan.md`

## Use this skill when

- Planning the next release version.
- Creating a new `vX.Y.Z_plan.md` from the master release plan.
- Reviewing which tasks from `RELEASE_PLAN_v1.md` apply to a specific version.

## Workflow

1. **Identify target version.**
   - Read `RELEASE_PLAN_v1.md` to find the current released version and the
     next planned milestone.
   - Confirm with the user which version to plan.

2. **Extract tasks from the master plan.**
   - Read the target milestone section in `RELEASE_PLAN_v1.md`.
   - For each task, identify:
     - governing ADRs and standards
     - current implementation status (check the appendix gap tables)
     - dependencies on other tasks or prior milestones

3. **Read governing ADRs.**
   - For each referenced ADR, read the full ADR and its appendix gap table.
   - Note which gaps are already closed vs. still open.

4. **Check current codebase state.**
   - For each task, identify the relevant source modules and their current
     implementation state.
   - Note any tasks already partially or fully completed.

5. **Draft the plan.**
   - Create `docs/improvement/vX.Y.Z_plan.md` following the structure of
     `references/version_plan_reference.md` and existing plans
     (v0.11.0_plan.md, v0.11.1_plan.md).
   - Each task section must include:
     - goal statement
     - relevant references (ADRs, standards, source files)
     - current status assessment
     - implementation steps (concrete, actionable)
     - verification checklist
   - Include a release gate summary at the end.

6. **Cross-check completeness.**
   - Verify every task from the master plan milestone has a section.
   - Verify every open gap from the appendix for referenced ADRs is addressed.
   - List minimal new tests required.

## Output contract

Produce `docs/improvement/vX.Y.Z_plan.md` with:
- header identifying version, milestone type, and authoritative task source
- source references reviewed
- global rules section (if applicable)
- numbered task sections matching the master plan
- release gate summary
- minimal new tests section

## Constraints

- Do not invent tasks not in `RELEASE_PLAN_v1.md` without explicit user approval.
- Do not modify `RELEASE_PLAN_v1.md` itself (use `ce-adr-author` for that).
- Mark tasks as completed only when verification evidence exists in the codebase.
- Respect the existing plan format conventions from v0.11.0_plan.md.
