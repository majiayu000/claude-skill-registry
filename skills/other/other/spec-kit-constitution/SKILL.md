---
name: spec-kit-constitution
description: Use when creating or amending a Spec Kit project constitution, especially when `memory/constitution.md` is missing, contains `[PLACEHOLDER]` tokens, or principle changes must be propagated to planning/spec/task templates.
---

# Spec Kit Constitution

Create or amend the project constitution and keep dependent templates aligned.

## When to Use

- User asks to create the first constitution for a Spec Kit project.
- User asks to amend governance/principles and update constitution versioning.
- `memory/constitution.md` is missing or still contains `[PLACEHOLDER]` tokens.
- Principle changes must be propagated into planning/spec/task templates.

## Router Fit

- Primary route from `spec-kit` when intent is governance/principles.
- Run before feature planning when constitutional rules changed.
- Downstream dependency: `spec-kit-plan` constitution checks rely on this output.

## Preconditions

- Work from the target project repository root.
- Treat `memory/constitution.md` as the source of truth once created.

## Workflow

1. Resolve constitution file:
   - Target: `{REPO_ROOT}/memory/constitution.md`.
   - If missing, initialize from `{REPO_ROOT}/templates/constitution-template.md` when present; otherwise use `assets/constitution-template.md`.
2. Capture baseline state from existing constitution (if present):
   - Current version.
   - Ratified and last amended dates.
   - Principle/section titles for diff reporting.
   - Any unresolved `[PLACEHOLDER]` tokens.
3. Fill required values from user input first, then repository context.
   - If critical data is unknown, use `TODO(<FIELD_NAME>): <reason>`.
4. Decide semantic version bump and dates:
   - `MAJOR`: backward-incompatible governance/principle redefinition or removal.
   - `MINOR`: new principle/section or materially expanded policy.
   - `PATCH`: clarifications, wording, typo, non-semantic refinements.
   - `RATIFICATION_DATE`: keep original adoption date.
   - `LAST_AMENDED_DATE`: set to today (`YYYY-MM-DD`) only when content changes.
5. Draft the constitution:
   - Replace placeholders with concrete policy text.
   - Keep heading hierarchy from the template.
   - Make principles declarative and testable (`MUST`/`SHOULD` with rationale).
   - Keep Governance explicit about amendment process, versioning policy, and compliance review.
6. Propagate policy changes to dependent templates in the target repo when present:
   - `templates/plan-template.md`
   - `templates/spec-template.md`
   - `templates/tasks-template.md`
     Update constitutional checks, required sections, and task expectations to match revised principles.
7. Prepend a Sync Impact Report HTML comment to `memory/constitution.md` containing:
   - Version change (`old -> new`).
   - Modified principles (including renames).
   - Added/removed sections.
   - Template sync status (`updated` vs `pending`) with file paths.
   - Deferred TODO items.
8. Validate before finalizing:
   - No unexplained bracket placeholders remain.
   - Version/date line matches report and uses `YYYY-MM-DD` format.
   - File path is `memory/constitution.md` (not `/memory/constitution.md`).
9. Write `memory/constitution.md` and report results to the user.

## Output

- Updated `memory/constitution.md`.
- Updated template files when present and required.
- Summary including version bump rationale, pending follow-ups, and a suggested commit message.

## Common Mistakes

- Updating principles without updating dependent templates.
- Using a patch bump for material policy changes that require a minor/major bump.
- Leaving unresolved placeholders without explicit TODO annotations.
- Writing to `/memory/constitution.md` instead of `memory/constitution.md`.

## References

- `references/spec-kit-workflow.dot` for where constitution work fits in the Spec Kit sequence.
- `assets/constitution-template.md`
- `assets/spec-template.md`
- `assets/plan-template.md`
- `assets/tasks-template.md`
- `https://github.com/github/spec-kit/blob/9111699cd27879e3e6301651a03e502ecb6dd65d/templates/commands/constitution.md`
