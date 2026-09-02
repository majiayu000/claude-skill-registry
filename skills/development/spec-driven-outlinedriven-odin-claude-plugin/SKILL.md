---
name: spec-driven
description: 'Use when starting a project or feature, requirements are unclear, or a change crosses modules. Produces an approved six-area spec, plan, tasks, and an offensive-first TDD implementation. Not for implementation from existing specs — use spec-driven-implementation.'
---

# Spec-driven development

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A new project or feature is starting, requirements are unclear, the change touches multiple modules, or the task exceeds roughly 30 minutes. |
| Authority | Reversible local: files, VCS, and credentials scoped to the current working tree; no remote mutation, credential exposure, or irreversible action. |
| Side effect | Writes and commits a spec, records human-approved plan and tasks, and implements through offensive-first TDD. All writes are local; no external service calls. |
| Done | A reviewed, approved spec covering six areas is saved to the repo and the implementation follows it. |

## Inputs

The user's request is mandatory. The requester must approve the spec before planning begins.

## Refusal

- Human withholds approval: do not proceed to the next phase. Surface the specific objection and wait.
- Scope widens mid-implementation: stop. Return to the spec. Update it; get approval; then proceed.
- Assumption surfaces after spec is written: surface it immediately; do not proceed until the human resolves or approves it.
- No spec written or saved: the done predicate is not met. Implement nothing until the spec exists and is approved.
- Non-converged: if the human never approves, the skill ends with no implementation. State this outcome explicitly.

## Procedure

1. **Surface assumptions first.** Before writing any spec content, list every assumption being made and require explicit correction. Do not silently fill ambiguous requirements. Done when: every assumption is listed and corrected or confirmed.
2. **Write the spec covering six core areas:**
   a. **Objective**: what is being built and why, who the user is, what success looks like.
   b. **Commands**: full executable commands with flags (build, test, lint, dev) for the stack the project actually uses. Record exact commands, not bare tool names.
   c. **Project structure**: where source lives, where tests go, where docs belong. Capture the layout that applies.
   d. **Code style**: one real snippet of the project's style beats paragraphs describing it. Include naming conventions, formatting rules, and an accepted example in the project's language.
   e. **Testing strategy**: sketch the seams where the feature will be tested. Prefer an existing seam to a new one; use the highest seam available; propose any new seam at the highest point where it can sit. Record the framework, test locations, coverage expectations, and which test level covers each concern. Confirm seams with the user before proceeding because a seam disagreement invalidates the testing strategy beneath it.
   f. **Boundaries**: three tiers — Always (run tests before commits, follow naming conventions, validate inputs); Ask first (schema changes, adding dependencies, changing CI config); Never (commit secrets, edit vendored directories, delete failing tests without approval).
   Done when: all six areas are written.
3. **Present the spec to the human.** Do not advance until the human reviews and approves it. The human's approval gates every subsequent phase. Done when: the human approves the spec.
4. **Plan from the validated spec.** Identify major components and dependencies; determine implementation order; note risks and mitigations; separate parallel from sequential work; define verification checkpoints. Done when: the plan is written.
5. **Present the plan to the human.** Do not advance until the human reviews and approves it. Done when: the human approves the plan.
6. **Break the plan into discrete tasks.** Each task: completable in one focused session; has explicit acceptance criteria; includes a verification step (test, build, or manual check); is ordered by dependency; changes no more than ~5 files. Done when: the task list is written.
7. **Present the task list to the human.** Do not advance until the human reviews and approves it. Done when: the human approves the task list.
8. **Implement through offensive-first TDD, one task at a time.** For each task: run the `tdd` skill's cycle — turn its acceptance criteria into attacks that must fail red for the right reason, implement until the attacks stop breaking the code, and never bend a test or fixture to reach green — then verify against the acceptance criteria before starting the next task. Load only the spec sections and source files the current task needs. Done when: every task is implemented and verified.
9. **Update the spec first when decisions change.** If the data model or scope changes, update the spec, then implement. Done when: the spec reflects the current decision.
10. **Commit the spec** to version control alongside the code. Reference the spec in each PR. Done when: the spec is committed.

## Output

A reviewed, approved spec saved to a file in the repository covering all six areas, a human-approved plan, a human-approved task list, and implementation that follows that spec through offensive-first TDD. The spec is a living document committed to version control.
