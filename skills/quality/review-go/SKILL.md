---
description: Comprehensive Go backend code review with optional parallel agents
name: review-go
disable-model-invocation: true
---

# Go Backend Code Review

## Arguments

- `--parallel`: Spawn specialized subagents per technology area
- Path: Target directory (default: current working directory)

## Step 1: Identify Changed Files

```bash
git diff --name-only $(git merge-base HEAD main)..HEAD | grep -E '\.go$'
```

**Pass condition:** If this prints nothing, state **No Go files in this diff** in the summary and **skip Steps 2–6**; do not invent findings for out-of-scope files.

## Step 2: Detect Technologies

```bash
# Detect BubbleTea TUI
grep -r "charmbracelet/bubbletea\|tea\.Model\|tea\.Cmd" --include="*.go" -l | head -3

# Detect Wish SSH
grep -r "charmbracelet/wish\|ssh\.Session\|wish\.Middleware" --include="*.go" -l | head -3

# Detect Prometheus
grep -r "prometheus/client_golang\|promauto\|prometheus\.Counter" --include="*.go" -l | head -3

# Detect ZeroLog
grep -r "rs/zerolog\|zerolog\.Logger" --include="*.go" -l | head -3

# Check for test files
git diff --name-only $(git merge-base HEAD main)..HEAD | grep -E '_test\.go$'
```

## Step 3: Load Verification Protocol

Load `beagle-go:review-verification-protocol` skill and keep its checklist in mind throughout the review.

## Step 4: Load Skills

Use the `Skill` tool to load each applicable skill (e.g., `Skill(skill: "beagle-go:go-code-review")`).

**Always load:**
- `beagle-go:go-code-review`

**Conditionally load based on detection:**

| Condition | Skill |
|-----------|-------|
| Test files changed | `beagle-go:go-testing-code-review` |
| BubbleTea detected | `beagle-go:bubbletea-code-review` |
| Wish SSH detected | `beagle-go:wish-ssh-code-review` |
| Prometheus detected | `beagle-go:prometheus-go-code-review` |

**Pass before Step 5:** You have loaded `beagle-go:go-code-review` (and Step 3 verification protocol). Load a **conditional** skill only when its row applies: `_test.go` in Step 1 diff → testing skill; BubbleTea/Wish/Prometheus skill only if the matching Step 2 `grep` returned at least one path (if `grep` returned nothing, do **not** load that skill).

## Step 5: Review

**Sequential (default):**
1. Load applicable skills
2. Review Go quality issues first (error handling, concurrency, interfaces)
3. Review detected technology areas
4. Consolidate findings

**Parallel (--parallel flag):**
1. Detect all technologies upfront
2. Spawn one subagent per technology area with `Task` tool
3. Each agent loads its skill and reviews its domain
4. Wait for all agents
5. Consolidate findings

## Step 6: Verify Findings

Before reporting any issue:
1. Re-read the actual code (not just diff context)
2. For "unused" claims - did you search all references?
3. For "missing" claims - did you check framework/parent handling?
4. For syntax issues - did you verify against current version docs?
5. Remove any findings that are style preferences, not actual issues

**Hard gates before listing any Critical or Major issue** (Informational may be lighter):

1. **Read-depth:** You opened the file on disk and read at least the enclosing function or block (diff-only or excerpt-only reading is not enough).
2. **Unused / dead code:** You ran a reference search (`rg`/IDE) and noted the result in the finding (e.g. no references outside tests), or you are not claiming unused symbols.
3. **“Missing” behavior:** You checked callers, framework wiring, or docs for the claimed gap, or you downgraded/dropped the item.

## Step 7: Review Convergence

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
   - Why: Why this matters (bug, race condition, resource leak, security)
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
go build ./...
go vet ./...
golangci-lint run
go test -v -race ./...
```

All checks must pass before approval.

## Rules

- Load skills BEFORE reviewing (not after)
- Number every issue sequentially (1, 2, 3...)
- Include FILE:LINE for each issue
- Separate Issue/Why/Fix clearly
- Categorize by actual severity
- Check for race conditions with `-race` flag
- Run verification after fixes
- Report ALL issues in a single pass — do not hold back findings for later iterations
- Re-reviews verify previous fixes ONLY — no new discovery
- Requests for net-new code (new modules, dependencies, test suites) are Informational, not blocking
- The Verdict ignores Minor and Informational items — only Critical and Major block approval
