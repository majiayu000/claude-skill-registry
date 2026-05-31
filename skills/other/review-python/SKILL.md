---
description: Comprehensive Python/FastAPI backend code review with optional parallel agents
name: review-python
disable-model-invocation: true
---

# Backend Code Review

## Hard gates (sequence)

Advance only when each **pass condition** is objectively satisfied (prevents linter-owned false positives and ungrounded findings):

| Gate | Pass condition |
|------|----------------|
| **G1 — Diff scope** | Step 1 command has been run; the changed `.py` paths are enumerated in writing (list may be empty — if empty, state that explicitly and do not invent Python findings). |
| **G2 — Linters before manual style/type** | For `ruff` and `mypy`: either no project config exists for that tool, **or** it was run on the changed files and you captured pass/fail (exit code or clear tool output). **Do not** add manual style or type findings for rules those tools already enforce when configured. |
| **G3 — Protocol and base skills** | `beagle-python:review-verification-protocol`, `beagle-python:python-code-review`, and `beagle-python:fastapi-code-review` are loaded before Step 6 substantive review. |
| **G4 — Evidence per issue** | Step 7 checks are satisfied for each reported issue before it appears in the final list (re-read source, search references for “unused”, confirm framework handling for “missing”, verify syntax against current docs). |
| **G5 — Output contract** | Findings use sequential numbering, every issue has `FILE:LINE`, and the **Verdict** follows Step 8 (Critical/Major only block; Minor/Informational do not). |

## Arguments

- `--parallel`: Spawn specialized subagents per technology area
- Path: Target directory (default: current working directory)

## Step 1: Identify Changed Files

**Pass (G1):** Capture the command output (or equivalent) as your authoritative changed-`.py` set before Steps 2–3.

```bash
git diff --name-only $(git merge-base HEAD main)..HEAD | grep -E '\.py$'
```

## Step 2: Verify Linter Status

**CRITICAL**: Run project linters BEFORE flagging any style or type issues. **Pass (G2):** You may only proceed to Step 3 after each configured linter has been run on the changed files or you have recorded why it was skipped (missing config).

```bash
# Check if ruff config exists and run it
if [ -f "pyproject.toml" ] || [ -f "ruff.toml" ]; then
    ruff check <changed_files>
fi

# Check if mypy config exists and run it
if [ -f "pyproject.toml" ] || [ -f "mypy.ini" ]; then
    mypy <changed_files>
fi
```

**Rules:**
- If a linter passes for a specific rule (e.g., line length), DO NOT flag that issue manually
- Linter configuration is authoritative for style rules
- Only flag issues that linters cannot detect (semantic issues, architectural problems)

**Why:** Analysis of 24 review outcomes showed 4 false positives (17%) where reviewers flagged line-length violations that `ruff check` confirmed don't exist. The linter's configuration reflects intentional project decisions.

## Step 3: Detect Technologies

```bash
# Detect Pydantic-AI
grep -r "pydantic_ai\|@agent\.tool\|RunContext" --include="*.py" -l | head -3

# Detect SQLAlchemy
grep -r "from sqlalchemy\|Session\|relationship" --include="*.py" -l | head -3

# Detect Postgres-specific
grep -r "psycopg\|asyncpg\|JSONB\|GIN" --include="*.py" -l | head -3

# Check for test files
git diff --name-only $(git merge-base HEAD main)..HEAD | grep -E 'test.*\.py$'
```

## Step 4: Load Verification Protocol

Load `beagle-python:review-verification-protocol` skill and keep its checklist in mind throughout the review.

## Step 5: Load Skills

Use the `Skill` tool to load each applicable skill (e.g., `Skill(skill: "beagle-python:python-code-review")`).

**Always load:**
- `beagle-python:python-code-review`
- `beagle-python:fastapi-code-review`

**Conditionally load based on detection:**

| Condition | Skill |
|-----------|-------|
| Test files changed | `beagle-python:pytest-code-review` |
| Pydantic-AI detected | `beagle-ai:pydantic-ai-common-pitfalls` |
| SQLAlchemy detected | `beagle-python:sqlalchemy-code-review` |
| Postgres detected | `beagle-python:postgres-code-review` |

## Step 6: Review

**Sequential (default):**
1. Load applicable skills
2. Review Python quality issues first
3. Review FastAPI patterns
4. Review detected technology areas
5. Consolidate findings

**Parallel (--parallel flag):**
1. Detect all technologies upfront
2. Spawn one subagent per technology area with `Task` tool
3. Each agent loads its skill and reviews its domain
4. Wait for all agents
5. Consolidate findings

### Before Flagging Optimization or Pattern Issues

1. **Check CLAUDE.md** for documented intentional patterns
2. **Check code comments** around the flagged area for "intentional", "optimization", or "NOTE:"
3. **Trace the code path** before claiming missing coverage or inconsistent handling
4. **Consider framework idioms** - what looks wrong generically may be correct for the framework

**Why:** Analysis showed rejections where reviewers flagged "inconsistent error handling" that was intentional optimization, and "missing test coverage" for code paths that don't exist.

## Step 7: Verify Findings

**Pass (G4):** No issue ships until all bullets below are true for that issue.

Before reporting any issue:
1. Re-read the actual code (not just diff context)
2. For "unused" claims - did you search all references?
3. For "missing" claims - did you check framework/parent handling?
4. For syntax issues - did you verify against current version docs?
5. Remove any findings that are style preferences, not actual issues

## Step 8: Review Convergence

**Pass (G5):** Final markdown matches the Output Format template; verdict line reflects only Critical/Major blockers per scope rules below.

### Single-Pass Completeness

You MUST report ALL issues across ALL categories (style, logic, types, tests, security, performance) in a single review pass. Do not hold back issues for later rounds.

Before submitting findings, ask yourself:
- "If all my recommended fixes are applied, will I find NEW issues in the fixed code?"
- "Am I requesting new code (tests, types, modules) that will itself need review?"

If yes to either: include those anticipated downstream issues NOW, in this review, so the author can address everything at once.

### Scope Rules

- Review ONLY the code in the diff and directly related existing code
- Do NOT request new features, test infrastructure, or architectural changes that didn't exist before the diff
- If test coverage is missing, flag it as ONE Minor issue ("Missing test coverage for X, Y, Z") — do NOT specify implementation details like mock libraries, behaviour extraction, or dependency injection patterns that would introduce substantial new code
- Typespecs, documentation, and naming issues are Minor unless they affect public API contracts
- Do NOT request adding new dependencies (e.g. Mox, testing libraries, linter plugins)

### Fix Complexity Budget

Fixes to existing code should be flagged at their real severity regardless of size.

However, requests for **net-new code that didn't exist before the diff** must be classified as Informational:
- Adding a new dependency (e.g. Mox, a linter plugin)
- Creating entirely new modules, files, or test suites
- Extracting new behaviours, protocols, or abstractions

These are improvement suggestions for the author to consider in future work, not review blockers.

### Iteration Policy

If this is a re-review after fixes were applied:
- ONLY verify that previously flagged issues were addressed correctly
- Do NOT introduce new findings unrelated to the previous review's issues
- Accept Minor/Nice-to-Have issues that weren't fixed — do not re-flag them
- The goal of re-review is VERIFICATION, not discovery

## Output Format

```markdown
## Review Summary

[1-2 sentence overview of findings]

## Issues

### Critical (Blocking)

1. [FILE:LINE] ISSUE_TITLE
   - Issue: Description of what's wrong
   - Why: Why this matters (bug, type safety, security)
   - Fix: Specific recommended fix

### Major (Should Fix)

2. [FILE:LINE] ISSUE_TITLE
   - Issue: ...
   - Why: ...
   - Fix: ...

### Minor (Nice to Have)

N. [FILE:LINE] ISSUE_TITLE
   - Issue: ...
   - Why: ...
   - Fix: ...

### Informational (For Awareness)

N. [FILE:LINE] SUGGESTION_TITLE
   - Suggestion: ...
   - Rationale: ...

## Good Patterns

- [FILE:LINE] Pattern description (preserve this)

## Verdict

Ready: Yes | No | With fixes 1-N (Critical/Major only; Minor items are acceptable)
Rationale: [1-2 sentences]
```

## Post-Fix Verification

After fixes are applied, run:

```bash
ruff check .
mypy .
pytest
```

All checks must pass before approval.

## Rules

- Load skills BEFORE reviewing (not after)
- Number every issue sequentially (1, 2, 3...)
- Include FILE:LINE for each issue
- Separate Issue/Why/Fix clearly
- Categorize by actual severity
- Run verification after fixes
- Report ALL issues in a single pass — do not hold back findings for later iterations
- Re-reviews verify previous fixes ONLY — no new discovery
- Requests for net-new code (new modules, dependencies, test suites) are Informational, not blocking
- The Verdict ignores Minor and Informational items — only Critical and Major block approval
