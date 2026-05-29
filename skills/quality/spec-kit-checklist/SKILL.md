---
name: spec-kit-checklist
description: Use when a Spec Kit feature has `spec.md` and you need a requirements-quality checklist (clarity, completeness, consistency, measurability, coverage), not implementation/runtime test cases.
---

# Spec Kit Checklist

Generate domain-specific checklists that evaluate requirement quality in Spec Kit artifacts.

## When to Use

- `spec.md` exists and you need a checklist to review requirement quality before implementation.
- You want a focused lens (for example UX, API, security, performance, accessibility) over requirement quality.
- You need to surface ambiguity, missing coverage, or weak acceptance criteria in writing.

## When Not to Use

- You are writing runtime tests, QA scripts, or implementation verification steps.
- `spec.md` does not exist yet (`spec-kit-specify` first).
- High-impact ambiguity must be resolved in-spec before checklist generation (`spec-kit-clarify`).
- You are generating executable tasks (`spec-kit-tasks`) or implementing tasks (`spec-kit-implement`).

## Router Fit

- Primary route from `spec-kit` when the intent is requirement-quality checklist generation.
- Can be run as a standalone quality pass after `spec-kit-specify`/`spec-kit-clarify` and before or during implementation.
- Output checklists feed the optional checklist gate in `spec-kit-implement`.

## Preconditions

- Run from repository root (or a subdirectory inside it).
- Active feature context resolves to one `specs/<feature>/` directory.
- `spec.md` exists for that feature.

## Workflow

1. Resolve feature paths and enforce the checklist prerequisite gate:

   - Run `scripts/check-prerequisites.sh --paths-only --json` exactly once.
   - Parse and retain `REPO_ROOT`, `FEATURE_DIR`, and `FEATURE_SPEC`.
   - If `FEATURE_SPEC` (`spec.md`) is missing, stop and route to `spec-kit-specify`.

2. Load checklist context:

   - Required: `spec.md`.
   - Optional when present: `plan.md`, `tasks.md`.
   - Extract only requirement-relevant content: requirements, acceptance criteria, edge/error cases, non-functional constraints, assumptions/dependencies.

3. Clarify checklist scope only when needed:

   - Ask up to 3 concise, high-impact questions if scope/risk/audience is unclear.
   - Skip questions already answered in user input or artifacts.
   - If ambiguity still blocks item quality, ask up to 2 targeted follow-ups (max 5 total).

4. Choose checklist file target:

   - Ensure `FEATURE_DIR/checklists/` exists.
   - Derive a short domain slug from intent (for example `ux`, `api`, `security`, `performance`).
   - Create a new file per run: prefer `<slug>.md`; if it exists, create `<slug>-2.md`, `<slug>-3.md`, etc.
   - Never overwrite existing checklist files.

5. Generate requirement-quality checklist items:

   - Treat each item as a "unit test for requirement writing," not implementation behavior.
   - Group items under quality categories as needed:
     - Requirement Completeness
     - Requirement Clarity
     - Requirement Consistency
     - Acceptance Criteria Quality / Measurability
     - Scenario and Edge-Case Coverage
     - Non-Functional Requirements
     - Dependencies and Assumptions
     - Ambiguities and Conflicts
   - Use `CHK###` IDs starting at `CHK001` and increment sequentially.
   - Keep items in question form and focused on what is documented or missing.

6. Apply strict item-quality rules:

   - Prefer patterns such as:
     - `Are <requirements> defined/specified for <scenario>?`
     - `Is <term> quantified with measurable criteria?`
     - `Are requirements consistent between <section A> and <section B>?`
   - Do not generate implementation checks (for example click/render/load/execute behavior checks).
   - Do not use runtime-verification framing (`Verify`, `Test`, `Confirm`) for system behavior.
   - Include traceability on most items (target: >=80%) using markers like `[Spec §...]`, `[Gap]`, `[Ambiguity]`, `[Conflict]`, `[Assumption]`.

7. Write output using template structure:

   - Preferred template: `{REPO_ROOT}/templates/checklist-template.md`.
   - Fallback template: `assets/checklist-template.md`.
   - Preserve heading order and emit checklist rows in this format:
     - `- [ ] CHK### <question> [markers]`

8. Validate before final report:

   - No implementation/runtime verification items.
   - IDs are unique and sequential.
   - Items are requirement-quality questions.
   - Traceability markers meet target coverage.

9. Report completion:

   - Absolute checklist path.
   - Item count.
   - Selected focus areas, depth/audience assumptions, and any explicit must-have user constraints incorporated.
   - Reminder that each run creates a new checklist file.

## Output

- New checklist file in `specs/<feature>/checklists/`.
- Requirement-quality checklist items with sequential `CHK###` IDs.
- Summary of scope assumptions and checklist focus.

## Key Rules

- Evaluate the quality of requirements writing, not whether implementation works.
- Keep items objective, reviewable, and traceable to artifacts.
- Prefer concise, high-signal checklists over exhaustive low-value lists.

## Common Mistakes

- Writing QA/runtime checks ("verify the API returns 200") instead of requirement-quality checks ("requirement specifies expected response codes").
- Producing vague items with no traceability marker.
- Overfitting to implementation details that do not belong in requirements artifacts.
- Overwriting an existing checklist instead of creating a new file for the run.

## References

- `scripts/check-prerequisites.sh`
- `assets/checklist-template.md`
- `https://github.com/github/spec-kit/blob/9111699cd27879e3e6301651a03e502ecb6dd65d/templates/commands/checklist.md`
