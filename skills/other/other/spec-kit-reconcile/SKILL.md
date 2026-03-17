---
name: spec-kit-reconcile
description: Use when specification drift is discovered at any stage and existing Spec Kit artifacts (`spec.md`, `plan.md`, `tasks.md`) must be reconciled in-place without creating a new feature branch.
---

# Spec Kit Reconcile

Close specification drift by updating existing Spec Kit artifacts in-place.

## When to Use

- You discover specification drift at any stage (specify, clarify, plan, tasks, analyze, or implement) and need artifacts realigned before continuing.
- Code exists, but behavior still misses expected flows (routing/navigation wiring, integration handoff, validation UX, coverage gaps).
- `spec-kit-analyze` found issues that require coordinated edits across `spec.md`, `plan.md`, and `tasks.md`.
- You need targeted remediation planning without creating a new feature branch.

## When Not to Use

- You need a brand-new feature spec (`spec-kit-specify` first).
- You need first-pass design decomposition from an approved spec (`spec-kit-plan` first).
- You only need a read-only audit (`spec-kit-analyze`).
- You are only executing already-correct tasks (`spec-kit-implement`).

## Router Fit

- First-class standalone remediation route when the developer identifies drift at any stage.
- Also serves as the default remediation handoff from `spec-kit-analyze` and `spec-kit-implement`.
- Produces reconciled artifacts and next-step routing based on the updated artifact state.

## Critical Constraints

- Never create a new feature branch and never run feature-creation scripts.
- Keep edits targeted; preserve artifact structure and heading order.
- Prefer append-only updates for `tasks.md`; do not renumber existing tasks.
- Run at most one clarification round (maximum 5 questions).
- Keep unresolved `NEEDS CLARIFICATION` markers to 3 or fewer.

## Preconditions

- Run from repository root (or a subdirectory inside it).
- Active feature context resolves to one `specs/<feature>/` directory.
- User provides a concrete gap report (symptoms, mismatches, missing wiring, and/or scope hints like `plan-only` or `tasks-only`).

## Workflow

1. Validate reconcile input:

   - If no gap report is provided, stop with `ERROR: No gap report provided`.
   - Parse user scope constraints (for example `spec-only`, `plan-only`, `tasks-only`) and preserve them throughout.

2. Resolve artifact paths exactly once:

   - Run `scripts/check-prerequisites.sh --json --paths-only --include-tasks` exactly once.
   - Parse:
     - `REPO_ROOT`
     - `BRANCH`
     - `FEATURE_DIR`
     - `FEATURE_SPEC`
     - `IMPL_PLAN`
     - `TASKS`
   - Validate required files:
     - If `FEATURE_SPEC` is missing, route to `spec-kit-specify`.
     - If `IMPL_PLAN` is missing, route to `spec-kit-plan`.

3. Load reconcile context:

   - Required: `spec.md`, `plan.md`.
   - Optional (when present): `tasks.md`, `data-model.md`, `contracts/`, `research.md`, `quickstart.md`.
   - Load `memory/constitution.md` and enforce its MUST-level constraints.
   - If `memory/constitution.md` is missing, stop and route to `spec-kit-constitution`.

4. Normalize the gap report into actionable items:

   - For each gap, capture:
     - `Title`
     - `Category`
     - `Evidence`
     - `Desired Outcome`
     - `Severity (HIGH|MEDIUM|LOW)`
   - Preferred categories:
     - `Navigation/Wiring`
     - `Integration/Contracts`
     - `Validation & UX`
     - `Authorization/Permissions`
     - `Test Coverage`
     - `Non-Functional`
     - `Docs`

5. Clarify once when needed:

   - Ask questions only when answers change scope, UX behavior, acceptance criteria, or remediation cost.
   - Ask at most 5 total questions in one round, then proceed.
   - If an `askQuestions`-style tool exists in the current runtime, prefer it for this step to collect all multiple-choice answers in one fast interaction.
   - When using `askQuestions`, provide 2-5 mutually exclusive options per question, put the recommended option first, and allow a short custom response path.
   - If no `askQuestions` tool exists, fall back to the markdown prompt format below.
   - Use this format for each question:

```markdown
## Question [N]: [Topic]

**Context**: [Relevant spec/plan/tasks excerpt or summary]
**Decision Needed**: [Single-sentence decision]
**Suggested Answers**:

| Option | Answer | Implications |
|--------|--------|--------------|
| A | [Option A] | [Impact] |
| B | [Option B] | [Impact] |
| C | [Option C] | [Impact] |
| Custom | Provide your own | [How it changes scope] |

**Your choice**: _[Wait for user response]_
```

6. Map impact per artifact:

   - `spec.md`: user stories, acceptance criteria, user-visible scenarios, edge behaviors.
   - `plan.md`: architecture/modules, routing/navigation, integration contracts, testing strategy.
   - `tasks.md`: remediation work with exact file paths and ordering.
   - Respect scope constraints and explicitly mark skipped artifacts.

7. Apply targeted edits:

   - `spec.md`:
     - Update only impacted sections.
     - Add a concise `Revisions` note (timestamp + reason).
   - `plan.md`:
     - Update only sections needed for reconciliation.
     - Keep design-level detail; do not add implementation patch instructions.
   - `tasks.md`:
     - If it exists, append remediation tasks using `NextID = max(T###) + 1`.
     - Preserve existing phases; add `Remediation: Gaps` phase when cross-cutting tasks are needed.
     - If it does not exist, create a minimal remediation-focused `tasks.md` from:
       1. `{REPO_ROOT}/templates/tasks-template.md`
       2. `{REPO_ROOT}/.specify/templates/tasks-template.md`
       3. fallback: `{REPO_ROOT}/skills/spec-kit-tasks/assets/tasks-template.md`
   - For wiring/flow gaps, always include integration test tasks.

8. Validate outputs:

   - No branch changes or feature-creation actions occurred.
   - Updated artifacts remain structurally valid and internally consistent.
   - Task formatting stays strict: `- [ ] T### [P?] [US#?] Action with exact file path`.

9. Report reconciliation result:

   - Provide a Sync Impact Report with:
     - changed files (absolute paths)
     - summary of edits by artifact
     - new task IDs
     - skipped artifacts due to scope constraints
     - outstanding `NEEDS CLARIFICATION` markers (maximum 3)
     - confirmation that constitution constraints were respected
   - Recommend next step based on gates (`spec-kit-plan`, `spec-kit-tasks`, or `spec-kit-implement`).

## Output

- Updated reconciliation artifacts (`spec.md`, `plan.md`, and/or `tasks.md`) in the active feature directory.
- New remediation tasks ready for execution.
- Sync Impact Report for traceability.

## Key Rules

- Keep reconciliation incremental and focused on stated gaps.
- Prefer appending over rewriting existing artifacts.
- Never reorder existing task IDs.
- Do not silently expand feature scope beyond the gap report and answered clarifications.

## Common Mistakes

- Running reconcile without a concrete gap report.
- Rewriting whole artifacts instead of targeted updates.
- Creating a new feature branch for remediation work.
- Adding vague remediation tasks without exact file paths or acceptance intent.
- Ignoring constitution MUST constraints while patching artifacts.

## References

- `scripts/check-prerequisites.sh`
- `references/spec-kit-workflow.dot`
- `https://github.com/github/spec-kit/issues/1063`
- `https://github.com/user-attachments/files/23166782/reconcile.md`
