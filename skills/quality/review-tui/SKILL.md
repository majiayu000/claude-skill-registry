---
description: Comprehensive BubbleTea TUI code review for terminal applications
name: review-tui
disable-model-invocation: true
---

# TUI Code Review

## Arguments

- `--parallel`: Spawn specialized subagents per technology area
- Path: Target directory (default: current working directory)

## Gates (sequence)

Advance only when each **pass condition** is true (reduces scope drift and unsubstantiated blocking claims):

| Gate | Pass condition |
|------|----------------|
| **G1 — Scope** | Step 1 produced a concrete list of target `.go` paths (from the git command or an explicit user path). If the list is empty, you **stopped** for scope clarification **or** recorded an agreed non-git scope (e.g. single file/dir) before reviewing. |
| **G2 — Skills before review** | `beagle-go:review-verification-protocol`, `beagle-go:go-code-review`, and `beagle-go:bubbletea-code-review` are loaded; Step 4 conditionals (tests → `go-testing-code-review`, Wish → `wish-ssh-code-review`) are loaded **before** Step 5. |
| **G3 — Evidence for Critical/Major** | Each Critical/Major finding cites **file path + line** (or a short quoted snippet) from the **opened** source—not from diff hunks alone. |
| **G4 — Pre-output hygiene** | Each retained finding was checked against Step 7 **and** the loaded verification protocol **before** writing the Issues section. |

Do not start Step 5 until **G2** passes. Do not publish Critical/Major until **G3** and **G4** pass.

## Step 1: Identify Changed Files

```bash
git diff --name-only $(git merge-base HEAD main)..HEAD | grep -E '\.go$'
```

## Step 2: Detect Technologies

```bash
# Detect BubbleTea (required for TUI review)
grep -r "charmbracelet/bubbletea" --include="*.go" -l | head -3

# Detect Lipgloss styling
grep -r "charmbracelet/lipgloss\|lipgloss\.Style" --include="*.go" -l | head -3

# Detect Bubbles components
grep -r "charmbracelet/bubbles\|list\.Model\|textinput\.Model\|viewport\.Model" --include="*.go" -l | head -3

# Detect Wish SSH server
grep -r "charmbracelet/wish\|ssh\.Session" --include="*.go" -l | head -3

# Check for test files
git diff --name-only $(git merge-base HEAD main)..HEAD | grep -E '_test\.go$'
```

## Step 3: Load Verification Protocol

Load `beagle-go:review-verification-protocol` skill and keep its checklist in mind throughout the review.

## Step 4: Load Skills

Use the `Skill` tool to load each applicable skill (e.g., `Skill(skill: "beagle-go:go-code-review")`).

**Always load:**
- `beagle-go:go-code-review`
- `beagle-go:bubbletea-code-review`

**Conditionally load based on detection:**

| Condition | Skill |
|-----------|-------|
| Test files changed | `beagle-go:go-testing-code-review` |
| Wish SSH detected | `beagle-go:wish-ssh-code-review` |

## Step 5: Review Focus Areas

### Model/Update/View (Elm Architecture)

- [ ] Model is immutable (Update returns new model)
- [ ] Init returns proper initial command
- [ ] Update handles all message types
- [ ] View is pure function (no side effects)
- [ ] tea.Quit used correctly for exit

### Lipgloss Styling

- [ ] Styles defined once at package level
- [ ] Styles not created in View function
- [ ] Colors use AdaptiveColor for light/dark themes
- [ ] Layout responds to WindowSizeMsg

### Component Composition

- [ ] Sub-component updates propagated
- [ ] WindowSizeMsg passed to resizable components
- [ ] Focus management for multiple components
- [ ] Clear state machine for view transitions

### SSH Server (if applicable)

- [ ] Host keys persisted
- [ ] Graceful shutdown implemented
- [ ] PTY window size passed to TUI
- [ ] Per-session Lipgloss renderer

## Step 6: Review

**Sequential (default):**
1. Load applicable skills
2. Review Go code quality
3. Review BubbleTea patterns (Model/Update/View)
4. Review Lipgloss styling
5. Review component composition
6. Review SSH server (if applicable)
7. Consolidate findings

**Parallel (--parallel flag):**
1. Detect all technologies upfront
2. Spawn subagents for: Go quality, BubbleTea, SSH
3. Wait for all agents
4. Consolidate findings

## Step 7: Verify Findings

Before reporting any issue:
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
   - Why: Why this matters (UI freeze, crash, resource leak)
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
- Pay special attention to:
  - Blocking operations in Update (freezes UI)
  - Style creation in View (performance)
  - Missing WindowSizeMsg handling (broken resize)
- Run verification after fixes
- Report ALL issues in a single pass — do not hold back findings for later iterations
- Re-reviews verify previous fixes ONLY — no new discovery
- Requests for net-new code (new modules, dependencies, test suites) are Informational, not blocking
- The Verdict ignores Minor and Informational items — only Critical and Major block approval
