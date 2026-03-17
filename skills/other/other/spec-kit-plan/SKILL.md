---
name: spec-kit-plan
description: Use when an approved Spec Kit `spec.md` must be translated into technical design artifacts (`plan.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`) before `spec-kit-tasks`, or when `plan.md` is missing/outdated after spec or constitution changes.
---

# Spec Kit Plan

Generate implementation design artifacts from the approved feature specification.

## When to Use

- `spec.md` exists and you need `plan.md` plus Phase 0/1 design outputs for task generation.
- `plan.md` is missing, stale, or invalid after changes to `spec.md` or `memory/constitution.md`.
- The next step is `spec-kit-tasks`, but technical context and design decisions are not yet documented.

## When Not to Use

- No usable `spec.md` exists yet (`spec-kit-specify` first).
- High-impact ambiguity in `spec.md` still blocks architecture or validation decisions (`spec-kit-clarify` first).
- You are decomposing design into executable work items (`spec-kit-tasks`).
- You only need a read-only consistency audit (`spec-kit-analyze`).
- You are reconciling cross-artifact drift discovered mid-work (`spec-kit-reconcile`).

## Router Fit

- Primary route from `spec-kit` after `spec-kit-specify` / `spec-kit-clarify`.
- Must complete before `spec-kit-tasks`.
- Depends on constitution output from `spec-kit-constitution`.

## Preconditions

- Work from the target repository root.
- Active feature branch resolves to a spec directory (`NNN-feature-name` format when git is available).
- `memory/constitution.md` exists and is current for planning gates.

## Workflow

1. Resolve active feature paths and initialize `plan.md`:

   - Run `scripts/setup-plan.sh --json` exactly once.
   - Parse and retain: `FEATURE_SPEC`, `IMPL_PLAN`, `SPECS_DIR`, `BRANCH`.
   - If the script exits non-zero (for example branch gate failure), stop and report the blocking error.

2. Enforce artifact gates before writing design outputs:

   - If `FEATURE_SPEC` (`spec.md`) is missing, stop and route to `spec-kit-specify`.
   - If `memory/constitution.md` is missing, stop and route to `spec-kit-constitution`.
   - If `spec.md` has unresolved high-impact ambiguity that can change architecture, data model, testing, UX, operations, or compliance, stop and route to `spec-kit-clarify`.

3. Load planning inputs with template fallback:

   - Required: `spec.md`, `memory/constitution.md`.
   - Preferred plan template: `{REPO_ROOT}/.specify/templates/plan-template.md`.
   - Fallback template: `assets/plan-template.md`.
   - Preserve template heading order; replace placeholders rather than adding parallel structures.

4. Draft `plan.md` core sections:

   - Complete Summary and Technical Context.
   - Mark unknown technical decisions as `NEEDS CLARIFICATION`.
   - Fill Constitution Check from `memory/constitution.md` with explicit pass/fail status.
   - Select one concrete project structure and remove unused template options.
   - Use Complexity Tracking only when a constitutional violation remains and is explicitly justified.

5. Run Phase 0 research (`research.md`):

   - Turn each `NEEDS CLARIFICATION` in Technical Context into a focused research question.
   - Record outcomes as:
     - `Decision`
     - `Rationale`
     - `Alternatives considered`
   - Resolve all blockers needed for design decisions before continuing.

6. Run Phase 1 design outputs:

   - Create/update `data-model.md` with entities, fields, relationships, validation rules, and state transitions where relevant.
   - Create/update `contracts/` for externally visible interfaces that the feature introduces or modifies.
   - Create/update `quickstart.md` with concrete validation flow for the designed feature.
   - Reflect final decisions back into `plan.md` so downstream task generation has a single source of truth.

7. Update agent context (explicit user approval required):

   - Before running the script, ask for explicit approval to update agent context files (for example `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.github/agents/copilot-instructions.md`).
   - Run `scripts/update-agent-context.sh` from repository root only after user approval.
   - If an agent type is provided by the user, pass it as the first argument.
   - If approval is declined or unavailable, skip this step and report it as skipped.
   - Report script failures explicitly; do not silently skip context updates.

8. Re-check gates and report completion:

   - Re-evaluate Constitution Check after Phase 1 outputs.
   - Stop with `ERROR` if unresolved constitutional violations or unresolved blocking clarifications remain.
   - Report `BRANCH`, absolute artifact paths, and readiness for `spec-kit-tasks`.

## Output

- `plan.md`:
  - Fully populated from the selected plan template.
  - Technical Context reflects final decisions from Phase 0.
  - Constitution Check is explicit (`pass`, `fail`, or justified exception).
  - Project Structure shows one concrete layout (no placeholder option blocks).
- `research.md`:
  - One entry per planning unknown using:
    - `Decision`
    - `Rationale`
    - `Alternatives considered`
  - Resolves all blocking `NEEDS CLARIFICATION` items required for design.
- `data-model.md`:
  - Captures entities, fields, relationships, validation constraints, and relevant state transitions.
  - Maps model decisions back to spec requirements where practical.
- `contracts/*` (when applicable):
  - Defines each new/changed external interface (endpoint/event/schema).
  - Includes input/output shape, validation/error behavior, and compatibility notes.
- `quickstart.md`:
  - Describes a concrete validation flow for the designed feature.
  - Covers primary success path plus key error/edge behavior from the spec.
- Updated agent context file(s) from `scripts/update-agent-context.sh` (only when user-approved):
  - Contains newly introduced technologies from the final plan.
  - Preserves user-maintained manual sections.
- If the user does not approve context updates:
  - Report that agent context sync was intentionally skipped.

## Key rules

- Use absolute paths in completion reporting.
- Treat missing prerequisites as hard stops with reroutes to the owning sibling skill.
- Do not generate `tasks.md` or implementation code in this skill.
- Keep plan artifacts at design granularity: architecture, data model, interfaces/contracts, constraints, and validation approach.
- Do not include execution-level content such as code snippets, patch-style file edits, command runbooks, or checklist task breakdowns.
- Do not leave blocking `NEEDS CLARIFICATION` unresolved by completion.
- Emit `ERROR` for unresolved constitution gates without justification.
- Never run `scripts/update-agent-context.sh` without explicit user approval in the current session.

## Common Mistakes

- Planning without an approved spec — the plan will lack stable requirements and churn.
- Using the wrong template source path (`spec-template` instead of `plan-template`).
- Keeping placeholder project-structure options in `plan.md` instead of selecting one concrete layout.
- Including execution details in plan artifacts (code snippets, exact commands, patch-level file changes, or task checklists) — design belongs in `spec-kit-plan`; execution belongs to `spec-kit-tasks` and `spec-kit-implement`.
- Skipping the post-design constitution re-check before handing off to `spec-kit-tasks`.
- Running context-file updates automatically without asking the user to approve changes to `AGENTS.md`/`CLAUDE.md`/related files.

## References

- `references/spec-kit-workflow.dot` for overall context of where planning fits in the Spec Kit sequence.
- `scripts/setup-plan.sh`
- `scripts/update-agent-context.sh`
- `assets/plan-template.md`
- `https://github.com/github/spec-kit/blob/9111699cd27879e3e6301651a03e502ecb6dd65d/templates/commands/plan.md`
