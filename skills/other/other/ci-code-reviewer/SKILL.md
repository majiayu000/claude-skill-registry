---
name: ci-code-reviewer
description: Automated CI code review for GitHub PRs using OpenAI Codex. Validates PR descriptions, checks implementation alignment, enforces Quest architecture boundaries, and maps test coverage to acceptance criteria when PRs move to ready-for-review.
---

# CI Code Reviewer

Automated code review for CI pipelines. Designed to run inside GitHub Actions
via `openai/codex-action`, producing a single structured PR comment.

This skill extends `.skills/code-reviewer/SKILL.md` with CI-specific
adaptations: no interactive prompts, PR description validation, manifest
pre-checks, and concise output formatting for automated comments.

---

## When to Use

Use this skill when:
- Running automated code review in GitHub Actions (Codex CI pipeline)
- Reviewing PRs that transition from draft to ready-for-review
- Performing non-interactive, autonomous code review

Do NOT use for:
- Interactive human-guided code review (use `code-reviewer` skill instead)
- Reviewing plans/specs (use `plan-reviewer` skill)
- Implementation tasks

---

## Required Context

Before starting the review, read:
1. `AGENTS.md` -- architecture boundaries and coding conventions
2. `.ai/context_digest.md` -- review priorities and testing expectations
3. `.skills/code-reviewer/SKILL.md` -- severity model and review baseline

If any file is missing, note it in the output and continue with available context.

---

## Severity Model (Use in PR Comments)

Classify findings using these levels, and include the level in each finding:

- **Blocker:** Merge must not proceed
- **Must fix:** Should be fixed before merge unless explicitly accepted as debt
- **Should fix:** Important, but can be deferred with clear rationale
- **Nit:** Ignore by default; mention only if specifically requested

Rule: avoid comment-only style polish and trivial corrections. Prefer high signal.

---

## Review Process

### Step 0: PR Description Validation (Mandatory)

This step is mandatory and must appear first in the output.

Check the PR description for:

1. **Good explanation**: WHAT changed and WHY it is needed.
2. **OR link/path to plan file**: for example `.quest/*/phase_01_plan/plan.md`
   or `docs/implementation/...`.

If neither condition is met:
- **Must fix**: "PR description is missing. Add what/why context or link to a readable implementation plan."

If description exists but is very thin (fewer than ~20 words, little context):
- **Should fix**: "PR description is sparse. Add more context about purpose and approach."

### Step 0.1: Manifest Validation (Mandatory)

Run `./scripts/validate-manifest.sh`.

- If it fails, flag **Must fix** with the failing file/path details.
- If PR adds or renames files under Quest-managed paths, verify `.quest-manifest`
  is updated in the diff.

### Step 0.5: Implementation Alignment

Verify that what the PR implements matches what it claims to do.
Use the best available source of intent, in priority order:

1. **Plan file** referenced in PR description (preferred)
2. **Acceptance criteria** listed in PR description
3. **PR description intent** (what + why) if no explicit AC

Missing plan file is not a reason to skip alignment. Fall back to description.

Compare expectations vs diff:
- Expected deliverable missing from diff -> **Must fix**
- Out-of-scope file changes not justified by tests/docs/config support -> **Should fix**
- Missing explicit acceptance criteria in PR description -> **Should fix**

For each acceptance criterion:
- Automated criterion missing code/test evidence -> **Must fix**
- Manual-only criterion -> mark `manual - not verified`
- Unclear from diff -> mark `unclear - needs human review`

If all criteria align, stay silent on this section.

### Step 1: Identify Changed Files and Scope

1. Run `git diff --name-only <base>...<head>`.
2. Run `git diff --stat <base>...<head>`.
3. Categorize changed files into:
   - Skills (`.skills/`, including `.skills/quest/`)
   - AI roles/config (`.ai/`)
   - Scripts (`scripts/`)
   - Workflows (`.github/workflows/`)
   - Documentation (`docs/`, `AGENTS.md`, quest markdown artifacts)

Use these categories to decide which boundary checks and quality checks apply.

### Step 2: Architecture Boundaries

Apply Quest boundaries from `AGENTS.md`:

- `.skills/`: skill definitions, review protocols, delegation docs
- `.ai/`: agent roles, templates, schemas, allowlist/context config
- `scripts/`: validation and utility shell scripts
- `.github/`: CI and repository automation config (especially workflow orchestration)
- `docs/`: documentation and guidance, no executable logic

For each changed file, verify:
- Changes stay within directory responsibility
- No cross-layer leakage (for example: embedding workflow logic into docs)
- Dependencies and references are appropriate to the layer

Boundary violations are **Must fix** or **Blocker** depending on severity.

### Step 3: Correctness and Contracts

Review for:
- Correct trigger/behavior semantics
- Config contract compatibility
- Data/config invariants
- Edge cases and failure semantics

Focus on behavior correctness, not style preferences.

### Step 4: Security Hygiene

PR-focused checks:
- No secrets in code, logs, or responses
- No sensitive data in errors
- Input/path validation at trust boundaries
- No hardcoded API keys or long-lived tokens

Secret leakage is always **Blocker**.

### Step 5: Test Coverage (Map to Acceptance Criteria)

If acceptance criteria are available from Step 0.5:
1. Map each automated criterion to tests or validation evidence.
2. If missing, flag as **Must fix**.

For workflow/config/skill-only changes, acceptable evidence can include:
- `./scripts/validate-manifest.sh`
- `./scripts/validate-quest-config.sh`
- Manual GitHub runtime verification steps when CI event behavior is required

If no criteria are available:
- Check that meaningful logic/config changes include corresponding validation
  updates or explicit rationale. Missing validation -> **Should fix**.

### Step 6: Code Quality and Maintainability

Review for clarity, maintainability, and consistency with existing patterns.

Markdown and YAML:
- Valid, consistent structure and headings
- Stable key names/ordering when convention exists
- No ambiguous indentation or malformed frontmatter

Shell scripts:
- Safe quoting and robust conditionals
- Avoid unsafe globbing and unbounded command behavior
- Portability and clear error handling

JSON/schema/config integrity:
- Schema references and paths are valid
- Config keys are spelled correctly and supported
- New files are registered where required (`.quest-manifest`, skill index)

Apply minimal diff principle: smallest correct change, no speculative refactors.

---

## Output Format

Keep output concise. Omit sections with no findings.

```
**PR Description:** PASS | FAIL - one-line explanation

**Summary:** 1-3 bullets. Recommendation: APPROVE / REQUEST CHANGES

**Findings** (only sections with issues):

**Blocker** - [path] Description and suggested fix
**Must fix** - [path] Description and suggested fix
**Should fix** - [path] Description and suggested fix

**Plan alignment** (only if gaps/scope creep found): list issues
**Test gaps** (only if gaps found): list missing coverage
**Architecture** (only if violations found): list violations
```

Line number guidance:
- Include `path:line` when the line comes from the diff.
- Otherwise use `path` alone.
- Do not guess line numbers.

Brevity rules:
- Clean review output should be short (PR description line + summary + APPROVE).
- Do not pad with empty PASS sections.
- Keep total output under 30 lines when possible.

---

## Principles

1. Correctness over style
2. Boundaries are enforced
3. Tests map to acceptance criteria
4. Security hygiene is non-negotiable
5. Minimal diff and high signal feedback
6. Autonomous operation (no interactive prompts)
7. Explicit severity on every finding
