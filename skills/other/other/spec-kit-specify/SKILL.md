---
name: spec-kit-specify
description: Use when a Spec Kit feature needs `spec.md` authored or rewritten from natural-language requirements, especially when the feature has no usable specification or requirements are too vague for planning.
---

# Spec Kit Specify

Create or refresh the feature specification for the active Spec Kit feature.

## When to Use

- Start a new feature and create the first `spec.md`.
- Convert free-form requirements into a structured, testable, implementation-agnostic specification.
- Rework an existing spec draft so it is ready for `spec-kit-clarify` or `spec-kit-plan`.

## When Not to Use

- Clarify ambiguity in an already-written spec without redrafting it (`spec-kit-clarify`).
- Generate design artifacts or tasks from an approved spec (`spec-kit-plan`, `spec-kit-tasks`).
- Reconcile cross-artifact drift in an existing feature (`spec-kit-reconcile`).

## Router Fit

- Primary route from `spec-kit` when `spec.md` does not exist yet.
- Downstream: hand off to `spec-kit-clarify` (if high-impact ambiguity remains) or `spec-kit-plan` (if spec is ready).

## Preconditions

- User provided a non-empty feature description.
- Run from repository root (or a subdirectory inside the repository).

## Workflow

01. Normalize input:

    - Treat the full user request as the feature description.
    - If empty, stop: `ERROR: No feature description provided`.

02. Generate a short branch suffix (2-4 words, kebab-case):

    - Preserve meaningful technical terms/acronyms.
    - Prefer action-noun phrasing (for example `user-auth`, `bulk-export-audit-log`).

03. Bootstrap feature branch and spec exactly once:

    - Run `scripts/create-new-feature.sh --json --short-name "<short-name>" "<feature description>"`.
    - Do not manually pre-compute branch numbers; let the script assign the next number.
    - Parse JSON output and capture:
      - `BRANCH_NAME`
      - `SPEC_FILE`
      - `FEATURE_NUM`
    - Derive `FEATURE_DIR` as `dirname(SPEC_FILE)`.

04. Load template context:

    - Preferred template: `{REPO_ROOT}/templates/spec-template.md`.
    - Fallback template: `assets/spec-template.md`.
    - Preserve heading order from the selected template.

05. Draft `spec.md` content (focus on WHAT/WHY, not HOW):

    - Fill prioritized user stories with independent tests and acceptance scenarios.
    - Write testable functional requirements.
    - Add edge cases and scope boundaries.
    - Add measurable, technology-agnostic success criteria.
    - Include key entities when data is central.
    - Use reasonable defaults and document assumptions when needed.

06. Clarification policy while drafting:

    - First, make informed defaults using domain norms.
    - Add `[NEEDS CLARIFICATION: ...]` only for high-impact uncertainty.
    - Hard limit: at most 3 clarification markers.
    - Prioritize by impact: scope > security/privacy > UX > technical detail.

07. Write the spec to `SPEC_FILE`.

08. Create and run requirements quality validation:

    - Create `FEATURE_DIR/checklists/requirements.md`.
    - Validate spec against this checklist:
      - No implementation details (frameworks, languages, APIs, internal architecture).
      - Mandatory sections are complete.
      - Requirements are unambiguous and testable.
      - Success criteria are measurable and technology-agnostic.
      - User scenarios and edge cases are covered.
      - Scope boundaries, dependencies, and assumptions are explicit.
      - No unresolved `[NEEDS CLARIFICATION]` markers for plan-ready specs.
    - If non-clarification issues fail, revise spec and re-validate (max 3 passes).

09. If clarification markers remain after validation:

    - Ask up to 3 numbered clarification questions total.
    - For each question, present 2-3 concrete options plus a short custom answer path.
    - Wait for user responses, update `spec.md`, then re-run validation.

10. Report completion:

- Branch name.
- `spec.md` path.
- `requirements.md` path and pass/fail summary.
- Recommended next step:
  - `spec-kit-clarify` if high-impact ambiguity remains.
  - `spec-kit-plan` if ready.

## Output

- Active feature branch from `scripts/create-new-feature.sh`
- `specs/<feature>/spec.md`
- `specs/<feature>/checklists/requirements.md`
- readiness handoff for `spec-kit-clarify` or `spec-kit-plan`

## Common Mistakes

- Writing implementation design into the spec instead of user-visible behavior and outcomes.
- Leaving vague requirements that cannot be acceptance-tested.
- Asking too many clarification questions instead of making reasonable defaults.
- Running feature bootstrap script multiple times for one request.

## References

- `references/spec-kit-workflow.dot`
- `scripts/create-new-feature.sh`
- `assets/spec-template.md`
- `https://github.com/github/spec-kit/blob/9111699cd27879e3e6301651a03e502ecb6dd65d/templates/commands/specify.md`
