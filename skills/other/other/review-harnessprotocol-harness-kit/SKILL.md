---
name: review
description: Use when user invokes /review to review code changes. Also triggers on "review my code", "check this PR", "look at my changes". Accepts a PR number (e.g. /review 123), a path filter (e.g. /review src/auth/), or no argument (reviews current branch vs base). Produces structured per-file review with severity labels, cross-file analysis, and an overall verdict. Do NOT use for explaining what code does — use /explain instead.
---

# Code Reviewer

## Overview

Produce structured code reviews for local branch changes, open PRs, or scoped paths. Designed to give concrete, actionable feedback — not a vague summary.

**Core principles:**
1. **Read-only.** Never modify files or post comments anywhere. Output goes to the conversation only.
2. **Concrete over vague.** Every concern includes a file path, line number if possible, and a specific issue. No "consider refactoring this" without saying exactly what and why.
3. **Severity matters.** Distinguish production-breaking blockers from style nits. Don't inflate every concern to a warning.
4. **No praise inflation.** "Straightforward rename, no concerns" is a complete review. Don't add empty praise.

## Invocation Examples

```
/review                    # review current branch vs base branch
/review 123                # review PR #123 via gh pr diff
/review src/auth/          # review changes scoped to a path
/review main...HEAD        # review with explicit git range
```

## Workflow Order (MANDATORY)

**You MUST follow this order. No skipping steps.**

---

### Step 1: Parse Input

Classify the argument:

| Input | Detection | Action |
|-------|-----------|--------|
| No argument | Empty / bare `/review` | Review current branch vs base using `git diff main...HEAD` |
| PR number | Numeric string (e.g. `123`) | Fetch diff with `gh pr diff 123` |
| Path filter | Looks like a file or directory path | Scope `git diff main...HEAD -- <path>` to that path |
| Git range | Contains `...` or `..` | Use directly as the git range |

If `gh` CLI is not available and user provided a PR number: say "gh CLI not found — run `brew install gh` and authenticate with `gh auth login` to review PRs by number. For local branch review, run `/review` without arguments." Then stop.

---

### Step 2: Gather Changes

Run the appropriate command to get the diff:

- **Local branch:** `git diff main...HEAD` (or `git diff $(git merge-base HEAD main)..HEAD` if the first fails)
- **PR number:** `gh pr diff <number>`
- **Path-scoped:** `git diff main...HEAD -- <path>`

If the diff is empty: say "No changes detected in [scope]. Make sure you're on a feature branch with committed changes." Then stop.

Parse the diff to identify:
- Which files changed
- Whether each change is an addition, deletion, or modification
- Approximate line numbers for changed sections

---

### Step 3: Classify Files

Categorize each changed file:

| Category | Examples |
|----------|---------|
| New logic | New functions, classes, services, handlers |
| Refactor | Moving/renaming code, changing interfaces |
| Test | `*_test.*`, `*.spec.*`, `test/**`, `__tests__/**` |
| Config | `*.json`, `*.yaml`, `*.toml`, `Makefile`, `Dockerfile` |
| Docs | `*.md`, `*.txt`, `docs/**` |
| Schema | Migrations, GraphQL schemas, Protobuf |

State the classification in the output — it tells the reader what kind of review to expect.

---

### Step 4: Per-File Review

For each changed file, produce a structured review block:

```
### <file path> (<category>)

**Summary:** One sentence: what changed and why (inferred from the diff).

**Concerns:**
- [BLOCKER] <specific issue with line reference> — <why this breaks things, suggested fix>
- [WARNING] <issue> — <why this matters>
- [NIT] <style/naming issue> — <suggested fix>

**Questions:**
- <anything unclear about the intent that a human author should clarify>

**Praise:** <one sentence max, only if genuinely noteworthy. Omit entirely if nothing stands out.>
```

Severity definitions:
- **BLOCKER** — Will cause a bug, crash, security issue, or data loss in production. Requires fix before merge.
- **WARNING** — Not immediately breaking but likely to cause problems: missing error handling, incorrect assumption, performance issue, missing test for critical path.
- **NIT** — Style, naming, minor clarity issue. Fine to address or ignore.

If a file has no concerns: write "No concerns." and move on. Don't invent issues.

---

### Step 5: Cross-File Analysis

After reviewing individual files, look across the whole changeset:

**Missing test coverage:** Are there new logic files with no corresponding test changes? Call them out specifically: "No test changes for `src/auth/validator.ts` — the new validation path is untested."

**Inconsistencies:** Do related files contradict each other? (e.g. an interface updated in one file but not in its implementor, a constant renamed in one place but not another)

**API contract changes:** Did any public interface, exported function signature, or API endpoint change? If yes, flag whether callers were updated.

**Unjustified dependencies:** Were any new packages added (`package.json`, `go.mod`, `requirements.txt`, etc.)? If yes, note them and ask why — each new dependency is a surface area and maintenance burden.

If nothing notable across files: write "No cross-file concerns."

---

### Step 6: Present Review

Output the complete review to the conversation in this order:

1. **Scope** — what was reviewed (branch/PR/path) and how many files changed
2. **Per-file reviews** (from Step 4)
3. **Cross-file analysis** (from Step 5)
4. **Overall verdict**

Overall verdict must be one of:
- **Approve** — No blockers. Warnings and nits noted above but not blocking.
- **Request Changes** — One or more BLOCKERs. List them again here for visibility.
- **Questions** — No blockers, but clarifying questions must be answered before verdict.

Example verdict block:
```
---
**Verdict: Request Changes**

Blockers:
- `src/payment/processor.ts:47` — integer overflow on amounts > 2^31 (see above)
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Vague concerns without line numbers | Always include file path. Include line number when visible in the diff. |
| Reviewing every file the same depth | Skim config/docs changes; focus depth on new logic and schema changes. |
| Inflating every issue to a blocker | Reserve BLOCKER for things that will actually break production. |
| Adding praise when there's nothing to say | Omit the Praise field entirely if nothing genuinely stands out. |
| Posting comments or modifying files | This skill is read-only. Output to conversation only. |
| Stopping because gh CLI is missing | Fall back to local diff mode. Only fail if user explicitly requested a PR number. |
