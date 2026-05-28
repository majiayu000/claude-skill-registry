---
description: Comprehensive Elixir/Phoenix code review with optional parallel agents
name: review-elixir
disable-model-invocation: true
---

# Elixir Code Review

## Arguments

- `--parallel`: Spawn specialized subagents per technology area
- Path: Target directory (default: current working directory)

## Hard gates

Complete in order before writing **Issues** in the output (empty scope is allowed; fabricated findings are not).

1. **Scope gate:** You have an explicit list of `.ex`/`.exs`/`.heex` paths under review (from Step 1 or user path). **Pass:** List printed or "No Elixir files in scope" — then stop with no Issues.
2. **Linter gate (style):** Step 2 commands ran for this Mix project; skipped tools are noted in one line (e.g. no `.credo.exs`). **Pass:** You do not report a style issue that already passes the project's formatter/linter for that line.
3. **Protocol gate:** `beagle-elixir:review-verification-protocol` is loaded before Step 6. **Pass:** At least one reported finding was checked against that checklist (state which item in the Review Summary or first Critical/Major note).
4. **Evidence gate (Critical/Major):** For each Critical or Major item, you re-read the file at `FILE:LINE` (full surrounding context, not only the diff hunk). **Pass:** The Issue description matches observable code at that location.

## Step 1: Identify Changed Files

```bash
git diff --name-only $(git merge-base HEAD main)..HEAD | grep -E '\.ex$|\.exs$|\.heex$'
```

## Step 2: Verify Linter/Formatter Status

**CRITICAL**: Run project linters BEFORE flagging any style issues.

```bash
# Check formatting
mix format --check-formatted

# Check Credo if present
if [ -f ".credo.exs" ] || grep -q ":credo" mix.exs 2>/dev/null; then
    mix credo --strict
fi

# Check Dialyzer if configured
if grep -q ":dialyxir" mix.exs 2>/dev/null; then
    mix dialyzer --format short
fi
```

**Rules:**
- If a linter passes for a specific rule, DO NOT flag that issue manually
- Linter configuration is authoritative for style rules
- Only flag issues that linters cannot detect (semantic issues, architectural problems)

## Step 3: Detect Technologies

```bash
# Detect Phoenix
grep -r "use Phoenix\|Phoenix.Router\|Phoenix.Controller" --include="*.ex" -l | head -3

# Detect LiveView
grep -r "use Phoenix.LiveView\|Phoenix.LiveComponent\|~H" --include="*.ex" -l | head -3

# Detect Oban
grep -r "use Oban.Worker\|Oban.insert" --include="*.ex" -l | head -3

# Check for test files
git diff --name-only $(git merge-base HEAD main)..HEAD | grep -E '_test\.exs$'
```

## Step 4: Load Verification Protocol

Load `beagle-elixir:review-verification-protocol` skill and keep its checklist in mind throughout the review.

## Step 5: Load Skills

Use the `Skill` tool to load each applicable skill.

**Always load:**
- `beagle-elixir:elixir-code-review`

**Conditionally load based on detection:**

| Condition | Skill |
|-----------|-------|
| Phoenix detected | `beagle-elixir:phoenix-code-review` |
| LiveView detected | `beagle-elixir:liveview-code-review` |
| Performance focus requested | `beagle-elixir:elixir-performance-review` |
| Security focus requested | `beagle-elixir:elixir-security-review` |
| Test files changed | `beagle-elixir:exunit-code-review` |

## Step 6: Review

**Sequential (default):**
1. Load applicable skills
2. Review Elixir quality issues first
3. Review Phoenix patterns (if detected)
4. Review LiveView patterns (if detected)
5. Review detected technology areas
6. Consolidate findings

**Parallel (--parallel flag):**
1. Detect all technologies upfront
2. Spawn one subagent per technology area with `Task` tool
3. Each agent loads its skill and reviews its domain
4. Wait for all agents
5. Consolidate findings

### Before Flagging Issues

1. **Check CLAUDE.md** for documented intentional patterns
2. **Check code comments** around the flagged area for "intentional", "optimization", or "NOTE:"
3. **Trace the code path** before claiming missing coverage
4. **Consider framework idioms** - what looks wrong generically may be correct for Elixir/Phoenix

## Step 7: Verify Findings

Satisfy **Hard gates** items 2–4 before finalizing Issues. Before reporting any issue:
1. Re-read the actual code (not just diff context)
2. For "unused" claims - did you search all references?
3. For "missing" claims - did you check framework/parent handling?
4. For syntax issues - did you verify against current version docs?
5. Remove any findings that are style preferences, not actual issues

## Step 8: Review Convergence

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

After fixes are applied, run the same checks as Step 2, then tests:

```bash
mix format --check-formatted

if [ -f ".credo.exs" ] || grep -q ":credo" mix.exs 2>/dev/null; then
    mix credo --strict
fi

if grep -q ":dialyxir" mix.exs 2>/dev/null; then
    mix dialyzer --format short
fi

mix test
```

All invoked checks must pass before approval.

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
