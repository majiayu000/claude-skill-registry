---
description: Reviews local changes, PRs/MRs, or branch diffs against project coding guidelines using 5 to 7 parallel review agents (bug detection, security/logic, guideline compliance x2, code simplification, test coverage, contract quality). Use before committing, on open PRs/MRs, or to review any branch diff. HIGH SIGNAL only: real bugs, logic errors, security concerns, and guideline violations. Supports a "deep" mode for iterative auto-fix — reviews and fixes code in a loop until clean.
disable-model-invocation: true
---

# Code Review

Analyze local git changes (or a PR/MR) against the project's coding guidelines, using 5 to 7 parallel review agents for comprehensive coverage. High-signal findings only: bugs, logic errors, security issues, guideline violations. Excludes style concerns, subjective suggestions, and linter-catchable issues.

## Step 1: Parse Arguments and Verify Prerequisites

### Parse invocation arguments

Extract from the user's arguments:
1. `deep` flag (present/absent)
2. `harness` keyword after `deep` (present/absent)
3. `--branch` flag (present/absent) — overrides Step 3's PR auto-route. Has no effect when local changes are present or when an explicit PR is requested (`--pr N`, `#N`, or a PR URL). Recorded as `force-branch-diff` for Step 3.
4. Everything else → scope/focus instructions (natural language, including PR numbers, paths, refs)

Examples:
- `/optimus:code-review` → local changes, normal mode
- `/optimus:code-review src/auth` → scope to path, normal mode
- `/optimus:code-review --pr 42` or `/optimus:code-review #42` → PR mode, normal
- `/optimus:code-review --branch` → branch diff against the detected base, skip PR auto-route
- `/optimus:code-review deep` → local changes, deep mode (8 iterations)
- `/optimus:code-review deep --branch` → branch diff against the detected base, deep mode
- `/optimus:code-review deep "focus on src/auth"` → scoped, deep mode
- `/optimus:code-review deep harness` → harness mode (present command and stop)
- `/optimus:code-review deep harness "focus on src/auth"` → harness mode, scoped

### Multi-repo workspace detection

Read `$CLAUDE_PLUGIN_ROOT/skills/init/references/multi-repo-detection.md` for workspace detection. If a multi-repo workspace is detected:
- Run the git commands below inside each child repo (the workspace root has no `.git/`, so git commands must target individual repos)
- For PR/MR mode, the user must specify which repo — PRs/MRs belong to individual repos
- If changed files cannot be mapped to any child repo (e.g., files at the workspace root), ask the user which repo's context to apply
- Prerequisite loading in Step 4 will resolve per-repo docs independently

### Documentation prerequisites

Read `$CLAUDE_PLUGIN_ROOT/skills/init/references/prerequisite-check.md` and apply the prerequisite check (CLAUDE.md + coding-guidelines.md existence, fallback logic).

## Step 2: Deep Mode Activation

### Harness mode detection

If the system prompt contains `HARNESS_MODE_ACTIVE`, read `$CLAUDE_PLUGIN_ROOT/references/harness-mode.md` and follow its single-iteration execution protocol. The reference covers progress file reading, state initialization, scope and file-list rules, Step 3 / Step 4 overrides under harness mode, and the Step 9 apply/output protocol. Then proceed through Step 3, Step 4, and Step 5 — skip only the Step 2 user confirmation.

If `HARNESS_MODE_ACTIVE` is NOT in the system prompt, continue with the standard interactive flow below.

### Skill-triggered harness invocation

If the `harness` keyword was detected in Step 1, read the **Skill-Triggered Invocation** section of `$CLAUDE_PLUGIN_ROOT/references/harness-mode.md` and follow its steps. Pass:
- `skill_name` = `code-review`
- `scope` = scope text from Step 1 argument parsing
- `max_iterations` = not specified (use harness default)

The reference protocol presents the command and stops. Do not proceed to Step 3 or any remaining steps.

### Interactive deep mode

If the `deep` flag was detected in Step 1 (without `harness`), activate deep mode. Deep mode loops review-fix cycles (Steps 5–9) until zero new findings remain or **8 iterations** are reached, then presents a single consolidated report with all fixes already applied as local changes.

Before proceeding, check whether a test command is available (from `.claude/CLAUDE.md`). If no test command exists, deep mode's auto-apply loop has no safety net — fall back to normal mode and warn: "Deep mode requires a test command for safe auto-apply. Falling back to normal mode — re-run `/optimus:init` to set up test infrastructure first." Then continue with the standard single-pass flow.

If a test command is available, warn the user:

> **Deep mode** runs up to 8 iterative review-fix passes. Each iteration is a full multi-agent review cycle — credit and time consumption multiplies with iteration count. Fixes are applied automatically at each iteration without per-change approval. Low test coverage increases the chance of undetected breakage; consider running `/optimus:unit-test` first to strengthen the safety net. Each iteration also accumulates context — on large codebases, output quality may degrade in later iterations.
>
> Test command: `[test command from CLAUDE.md]`

Then use `AskUserQuestion` — header "Deep mode", question "Proceed with deep mode?":
- **Start deep mode** — "Run iterative review-fix until clean (max 8 iterations)"
- **Normal mode** — "Single pass with manual approval instead"

Tell the user: *Tip: For large codebases or extended sessions, re-run with `/optimus:code-review deep harness` to launch the external harness with fresh context per iteration.*

If the user did not invoke with `deep`, skip this step.

If the user selects **Normal mode**, continue with the standard single-pass flow. Record the user's choice as a `deep-mode` flag for subsequent steps. If deep mode is confirmed, initialize `iteration-count` to 1, `total-fixed` to 0, `total-reverted` to 0, and `accumulated-findings` to an empty list. Each entry in `accumulated-findings` tracks: **file** (with line), **category** (Bug, Security, Guideline Violation, Code Quality, Test Coverage Gap, Contract Quality), **guideline** (the specific project rule, or "General: bug/security/contract quality"), **summary** (one-sentence description of the issue), **fix description** (brief description of the fix applied or attempted), **iteration** (which iteration discovered it), and **status** (updated through apply/test phases).

## Step 3: Determine Review Scope

Detect and gather the changes to review. Use the scope/focus instructions parsed in Step 1.

### Local changes (default flow)

Run the following git commands to gather all local changes:

```bash
# Staged changes
git diff --cached --stat
git diff --cached

# Unstaged changes to tracked files
git diff --stat
git diff

# Untracked files
git status --short
```

- **If local changes found** → review them (staged + unstaged + untracked)
- **If no local changes** → detect the comparison base and check for commits ahead:
  1. **Detect platform** — read `$CLAUDE_PLUGIN_ROOT/skills/pr/references/platform-detection.md` and use the **Platform Detection Algorithm** section to determine if the project is GitHub, GitLab, or unknown.
  2. **Detect PR/MR target branch** — check if an open PR/MR exists for the current branch and extract its target branch:
     - If GitHub: `gh pr view --json number,state,baseRefName 2>/dev/null` — only use `number` and `baseRefName` if `state` equals `"OPEN"`; if `state` is not `"OPEN"`, treat as "no open PR"
     - If GitLab: `glab mr view --output json 2>/dev/null` — only use `iid` and `target_branch` if `state` equals `"opened"`; if `state` is not `"opened"`, treat as "no open MR". If the command fails, treat as no open MR — unless the failure appears to be an auth or connectivity error, in which case inform the user before falling back
     - If platform unknown: try both, ignore CLI-unavailable errors — use the first result where an open PR/MR is confirmed (state check passed)
     - If no open PR/MR found or CLI unavailable → detect the default branch using `$CLAUDE_PLUGIN_ROOT/skills/pr/references/default-branch-detection.md`
  3. Use the detected branch as `<base-branch>` and capture the current branch as `<current-branch>` via `git rev-parse --abbrev-ref HEAD`. Run `git log --oneline origin/<base-branch>..HEAD`
  4. If commits found → route to the appropriate review mode (do NOT prompt the user to choose). Each branch diff route below jumps to the **Branch/ref mode** block using `origin/<base-branch>` as `<ref>`. For GitLab, substitute "MR !N" for "PR #N" in the user-facing notices below:
     - **`force-branch-diff` is set (from Step 1)** → review the branch diff.
     - **An open PR/MR was found AND HEAD is fully pushed** (`git rev-list origin/<current-branch>..HEAD` exits 0 with no output) → auto-enter PR mode for that PR. Reuse the PR/MR identifier captured in sub-step 2 above — jump to the **PR mode (explicit request)** block below without re-prompting. Tell the user, in one line: *"Reviewing PR #N — using the PR description as author intent context. Pass `--branch` to review the branch diff instead."*
     - **An open PR/MR was found BUT HEAD has unpushed commits or pushed state cannot be determined** (`git rev-list` returns lines or exits non-zero) → review the branch diff. Tell the user, in one line: *"Reviewing the branch diff — PR #N exists but HEAD is not fully pushed. Pass `--pr N` to review only the PR's pushed state."*
     - **No open PR/MR found (or CLI unavailable)** → review the branch diff.
- **If nothing at all** → inform the user there are no changes to review and suggest staging changes or specifying a PR

### PR mode (explicit request)

When the user says "review PR #42", passes `--pr`, `#123`, or a PR URL:

**Platform detection** — read `$CLAUDE_PLUGIN_ROOT/skills/pr/references/platform-detection.md` and use the **Platform Detection Algorithm** section (including the **Signal Conflict Resolution** rule). If platform is unknown → inform the user and ask them to specify.

**GitHub projects:**
- Verify `gh` is available by running `gh --version`. If not available, inform the user that PR review requires the GitHub CLI (`gh`) and offer to review the branch diff instead
- Use `gh pr view <N> --json state,isDraft,title,body,baseRefName,headRefName` to get PR metadata
- Store the `title` and `body` fields as `pr-description` for use in Steps 5 and 6 (author intent context)
- Use `gh pr diff <N>` to get the actual diff
- If the PR is closed or merged → warn and stop

**GitLab projects:**
- Verify `glab` is available by running `glab --version`. If not available, inform the user: "This project uses GitLab. PR/MR review requires the GitLab CLI (`glab`). You can use branch diff mode instead: `/optimus:code-review changes since origin/main`." Offer to review the branch diff as a fallback.
- Use `glab mr view <N> --output json` to get MR metadata
- Store the `title` and `description` fields as `pr-description` for use in Steps 5 and 6 (author intent context)
- Use `glab mr diff <N>` to get the actual diff
- If the MR is closed or merged → warn and stop

### Branch/ref mode

When the user says "review changes since main" or a similar reference:
- Use `git diff <ref>...HEAD` for the diff
- Use `git diff --name-only <ref>...HEAD` for the file list

### Path filter

When the user specifies a path (e.g., "review src/auth"):
- Filter local changes to that path using `git diff -- <path>` and `git diff --cached -- <path>`

### Scope summary

Present a brief summary before proceeding:

```
## Review Scope
- Mode: Local changes / PR #N / Branch diff since <ref>
- Files changed: [N]
- Lines: +[added] / -[removed]
```

### Large diff warning

If more than 50 files or 3000 lines are changed, warn the user and suggest narrowing the scope (e.g., specific path or directory).

## Step 4: Load Project Context

### Multi-repo workspace prerequisite loading

If a multi-repo workspace was detected in Step 1, resolve prerequisites per-repo:
- Determine which repo(s) the changed files belong to (from the diff file paths gathered in Step 3)
- Load each repo's `.claude/CLAUDE.md` and `.claude/docs/` independently (not the workspace root)
- If changes span multiple repos, apply per-repo context when reviewing that repo's files

### Load constraint docs

Read `$CLAUDE_PLUGIN_ROOT/skills/init/references/constraint-doc-loading.md` for the full document loading procedure (single project and monorepo layouts, scoping rules).

These files define the review criteria. Every guideline-related finding must be justified by what these docs establish — never impose external preferences.

### Exclude git submodules

Apply the "Submodule Exclusion" rule from `$CLAUDE_PLUGIN_ROOT/skills/init/references/constraint-doc-loading.md` — exclude submodule directories from the review.

### Context summary

Before proceeding to the review, present a brief summary:
- Docs loaded (with paths)
- Docs missing (with fallback status)
- Project type (single project / monorepo / multi-repo workspace)

Proceed immediately to Step 5 — do not wait for user confirmation.

## Step 5: Parallel Multi-Agent Review (5–7 agents)

Launch every applicable agent as a `general-purpose` Agent tool call in a **single** message so they run in parallel. The full fan-out is the design — do not reduce the count to save tokens or time. See the agent overview below for which agents always run and which activate conditionally.

Each agent receives the list of changed file paths (from Step 3 in normal/interactive mode, or from `scope_files.current` in harness mode when pre-populated by the harness).

Read the agent prompt files from `$CLAUDE_PLUGIN_ROOT/skills/code-review/agents/` for individual agent prompts. Read `$CLAUDE_PLUGIN_ROOT/skills/code-review/agents/shared-constraints.md` for the shared quality bar, exclusion rules, and false positive guidance applying to all agents.

### PR/MR context injection (PR/MR mode only)

If a `pr-description` was captured in Step 3 and its body is non-empty, prepend the PR/MR context block to every agent prompt before the file list. Read `$CLAUDE_PLUGIN_ROOT/skills/code-review/agents/context-blocks.md` for the template, truncation rule, and guardrail language.

### Iteration context injection (deep mode, iterations 2+)

If deep mode is active and `iteration-count` > 1, prepend the iteration context block to every agent prompt before the file list (after the PR/MR context block, if present). Read `$CLAUDE_PLUGIN_ROOT/skills/code-review/agents/context-blocks.md` for the template and format.

### Agent overview

| Agent | Role | Prompt file |
|-------|------|-------------|
| 1 — Bug Detector | Null access, off-by-one, race conditions, resource leaks, type mismatches | `bug-detector.md` |
| 2 — Security & Logic | SQL injection, XSS, hardcoded secrets, missing auth, security-relevant API violations | `security-reviewer.md` |
| 3 — Guideline Compliance A | Explicit violations of project docs with exact rule citations | `guideline-reviewer.md` |
| 4 — Guideline Compliance B | Same task as Agent 3 — independent review reduces false negatives | `guideline-reviewer.md` |
| 5 — Code Simplifier | Unnecessary complexity, naming, dead code, pattern violations | `code-simplifier.md` |
| 6 — Test Guardian | Test coverage gaps, structural barriers to testability | `test-guardian.md` |
| 7 — Contracts Reviewer | Backward compatibility, type safety, contract versioning, encapsulation | `contracts-reviewer.md` |

Agents 1–5 always run. Agent 6 (Test Guardian) runs when test infrastructure is detected (`.claude/docs/testing.md` or subproject `docs/testing.md` exists). Agent 7 (Contracts Reviewer) runs when changed files include contract-related paths (see activation rules below). Each agent returns a structured list of findings, bounded by the Finding Cap rule in `$CLAUDE_PLUGIN_ROOT/references/shared-agent-constraints.md`. Guideline agents (3–4) are constructed dynamically based on Step 4's doc loading results (single project vs monorepo paths).

### Contracts Reviewer activation (Agent 7)

Agent 7 activates when **any** changed file from Step 3 matches at least one of these patterns:

**Directory patterns** — file path contains any of: `api/`, `routes/`, `controllers/`, `endpoints/`, `handlers/`, `graphql/`, `proto/`, `grpc/`

**File patterns** — file name matches any of: `*.dto.*`, `*.schema.*`, `*.contract.*`, `openapi.*`, `swagger.*`, `*.proto`, `*.graphql`, `*.gql`

If no changed file matches, skip Agent 7 entirely (zero cost).

Wait for all launched agents to complete before proceeding to Step 6.

## Step 6: Validate Findings

Independently verify each finding to filter false positives. Apply the verification protocol from `$CLAUDE_PLUGIN_ROOT/skills/init/references/verification-protocol.md` — treat agent-reported findings as claims that require independent evidence, not as ground truth.

For each finding from Step 5:
1. **Context check** — read ±30 lines around the flagged location to verify the issue exists in context
2. **Intent check** — look for comments, test assertions, or established patterns that explain the code's behavior (what looks like a bug may be intentional)
3. **Pre-existing check** — verify the issue was introduced by the changes, not pre-existing in unchanged code
4. **Cross-agent consensus** — for guideline findings, check if both Agents 3 and 4 flagged the same issue (consensus = higher confidence)
5. **Runtime assumption check** — if an agent flagged a changed function or endpoint, verify whether the code also assumes something about inputs, dependencies, or environment that is not validated or documented. Unvalidated assumptions that could cause runtime failures strengthen the finding's confidence. (This is distinct from the verification protocol's Assumption Check, which targets pre-commitment design decisions.)

### Change-intent awareness

For each unique file that has findings, check recent git history for deliberate changes:

```bash
git log --no-merges --format="%h %s" -5 -- <file>
```

If a recent commit message clearly indicates deliberate code introduction (e.g., "fix null check", "add input validation", "harden auth flow") **and** a finding suggests removing or reverting that code → reduce the finding's confidence by one level (High → Medium, Medium → Low → drop).

For uninformative commit messages (fewer than 15 characters, or generic like "fix", "update", "changes"), run `git show <sha> -- <file>` to examine the actual diff for intent patterns: added null checks, validation logic, error handling, or security measures. Apply the same confidence reduction if the diff shows deliberate defensive code that a finding wants to remove.

### PR/MR description as intent signal

If a `pr-description` was captured in Step 3 (PR/MR mode), use it as an additional intent signal during validation:

- If the PR/MR description explicitly explains **why** a flagged change was made (e.g., "moved validation to middleware" explains removed validation) **and** git history corroborates it → apply one confidence reduction (same as change-intent above)
- If the PR/MR description claims intent but git history contradicts it or shows no supporting evidence → trust git history over the description (code over claims)
- If the PR/MR description is silent about a finding → no adjustment (absence of explanation is not evidence of intent)

This is a **soft adjustment only** — it never hard-filters a finding. It reduces the chance of undoing deliberate previous work while still allowing genuinely problematic code to be flagged. The PR/MR description and git history are complementary signals — neither alone can suppress a finding.

Skip gracefully if `git log` fails or returns no results (e.g., shallow clone, newly created file, or file outside the repository).

### Confidence assignment

Assign confidence:
- **High** — clear issue with strong evidence → keep
- **Medium** — plausible issue, some evidence → keep with note
- **Low** — uncertain, likely false positive → drop

Only findings with High or Medium confidence proceed to Step 7.

## Step 7: Consolidate and Present Findings

Merge validated findings from Steps 5–6. Deduplicate: if two agents flagged the same file and line range for the same category, keep the more detailed version. For guideline findings flagged by both Agents 3 and 4, merge into one finding and note "confirmed by independent review".

### Contradiction resolution

After deduplication, check for **cross-agent contradictions** — findings that target the same code region but recommend opposite directions (e.g., "add more validation" vs. "simplify this validation"). Keep the higher-severity finding and drop the other. When severities are equal, keep the security/correctness finding — security requirements justify proportionate complexity.

### Change Summary

Before presenting findings, write a concise summary (2–4 sentences) of what the reviewed changes accomplish. Describe the intent and effect of the changes — what was added, modified, or removed and why. Base this on the diff and the agents' analysis. This lets the user verify the review understood their changes correctly.

### Severity

- **Critical** — Bugs, security vulnerabilities, runtime failures
- **Warning** — Guideline violations, missing error handling, test coverage gaps for critical paths, backward-incompatible contract changes
- **Suggestion** — Code quality improvements, minor guideline drift, test coverage gaps for non-critical paths, minor contract quality issues

### Finding cap

Maximum **15 findings** across all sources, prioritized by severity then confidence. If more issues exist, note the count (e.g., "15 of ~24 findings shown") and suggest re-running with a narrower scope or using `/optimus:code-review deep` for exhaustive review.

### Deep mode accumulation

**Deep mode:** Instead of presenting the output format below, append this iteration's validated findings to `accumulated-findings`. For each appended finding, record the current `iteration-count` as the finding's iteration number, and preserve the agent's guideline citation and issue description as the finding's guideline and summary fields. Deduplicate against previous iterations: if a finding matches an existing entry by file + line range + category, skip it if the existing entry is marked "(fixed)". If the existing entry is marked "(persistent — fix failed)", annotate the new entry as "(persistent — fix failed)". If the existing entry is marked "(reverted — test failure)", keep the new entry as "(reverted — attempt 2)" so Step 9 retries the fix once more; only promote to "(persistent — fix failed)" if it is reverted again. Then proceed directly to Step 9.

**Normal mode:** Present findings using the output format below, then proceed to Step 8.

### Output format

```
## Code Review

### Summary
- Scope: [local changes / PR #N / branch diff since X]
- Files reviewed: [N]
- Lines changed: +[A] / -[R]
- Findings: [N] (Critical: [N], Warning: [N], Suggestion: [N])
- Docs used: [list of docs loaded]
- Agents: bug-detector, security-reviewer, guideline-A, guideline-B, code-simplifier[, test-guardian][, contracts-reviewer]
- Verdict: CHANGES LOOK GOOD / ISSUES FOUND

### Change Summary
[2–4 sentences describing what the changes do — their intent, what was added/modified/removed, and the overall effect. Keep it factual and concise.]

### Findings

**[N]. [Finding title]** (Critical/Warning/Suggestion — [Bug/Security/Guideline/Quality/Test Gap/Contract])
- **File:** `file:line`
- **Category:** [Bug | Security | Guideline Violation | Code Quality | Test Coverage Gap | Contract Quality]
- **Guideline:** [which project guideline, or "General: bug/security/contract quality"]
- **Issue:** [concrete description]
- **Current:**
  ```
  [code snippet — max 5 lines]
  ```
- **Suggested:**
  ```
  [fix or recommendation — max 5 lines]
  ```

[Findings ordered: Critical → Warning → Suggestion, each sorted by file path]

### No Issues Found
[If applicable: "The changes follow project guidelines. No bugs, security issues, or guideline violations detected."]
```

For PR mode, include full-SHA code links:
- **GitHub:** `https://github.com/owner/repo/blob/[full-sha]/path#L[start]-L[end]`
- **GitLab:** Extract the instance URL from `git remote get-url origin` (e.g., `https://gitlab.company.com`), then use: `https://[gitlab-host]/owner/repo/-/blob/[full-sha]/path#L[start]-L[end]`

## Step 8: Offer Actions (Normal Mode)

**Deep mode:** Skip this step — proceed directly to Step 9.

If the verdict is **CHANGES LOOK GOOD** (no findings), skip this step — do not present any action prompt. Go directly to the recommendation in the "Important" section below.

If the verdict is **ISSUES FOUND**, use `AskUserQuestion` to present actions. The options depend on the review mode determined in Step 3:

### Local changes / branch diff mode

Use `AskUserQuestion` — header "Action", question "How would you like to proceed with the review findings?":
- **Fix issues** — "Apply suggested fixes directly, then run tests to verify"
- **Skip** — "Keep the report as reference only"

### PR/MR review mode

Use `AskUserQuestion` — header "Action", question "How would you like to proceed with the review findings?":
- **Fix issues** — "Apply suggested fixes directly, then run tests to verify"
- **Post comment** — "Post the review summary as a PR/MR comment"
- **Skip** — "Keep the report as reference only"

Write the review summary to a secure temp file: `TMPFILE=$(mktemp "${TMPDIR:-/tmp}/review-summary-XXXXXX.md")`. Always clean up after the posting attempt (whether it succeeds or fails): `rm -f "$TMPFILE"`.

For GitHub PRs: `gh pr comment <N> --body-file "$TMPFILE"`
For GitLab MRs: `glab api -X POST "projects/:id/merge_requests/<N>/notes" -F body=@"$TMPFILE"` — this avoids shell metacharacter issues that `glab mr note --message "$(cat ...)"` would have with code snippets in the summary

## Step 9: Apply and Iterate (Deep Mode)

**Normal mode:** Skip this step.

### Convergence check

If zero findings were added to `accumulated-findings` in this iteration (Step 7 found nothing new), deep mode has converged. Report: "Deep mode complete — no new findings on iteration [N]." Skip to the **Consolidated report** below.

### Apply fixes

Apply all validated findings from this iteration using Edit or MultiEdit, skipping any annotated "(persistent — fix failed)" (these have already failed in a prior iteration). For each fix, record which file was modified and what the pre-edit content was (you will need this for revert if tests fail).

### Test and verify

Run the project's test command (from `.claude/CLAUDE.md`). Follow the verification protocol from `$CLAUDE_PLUGIN_ROOT/skills/init/references/verification-protocol.md` — run tests fresh, read complete output, report actual results with evidence.

- **If tests pass** → all fixes are valid. Annotate each applied finding as "(fixed)" in `accumulated-findings`. Add the count of applied fixes to `total-fixed`.
- **If tests fail** → revert all changes from this iteration, then re-apply fixes one at a time with a test run after each. Keep fixes that pass, skip those that fail. For each failed fix: if the finding is already annotated "(reverted — attempt 2)", promote it to "(persistent — fix failed)"; otherwise record it as "(reverted — test failure)". Add kept fixes to `total-fixed` and failed fixes to `total-reverted`.

### Termination check

After applying fixes and running tests, check termination conditions in order:

1. **All fixes this iteration were reverted** due to test failures → stop to prevent a loop of failed attempts. Report: "Deep mode stopped — all fixes in iteration [N] caused test failures."
2. **No fixes were applied** (all findings lacked actionable code edits) → stop. Report: "Deep mode stopped — remaining findings require manual review."
3. **`iteration-count` equals 8** → cap reached. Report: "Deep mode reached the iteration cap (8). Remaining findings may exist — continue in a fresh conversation: re-run `/optimus:code-review deep`, or narrow scope with `/optimus:code-review deep \"focus on <area>\"`."
4. **Otherwise** → continue to the next pass (iteration report and loop-back below).

**For all four conditions above**, present the iteration report immediately after the termination/continuation message. This report is informational and non-blocking — no user prompt follows:

```
#### Iteration [N] — Report

| # | File | What Changed | Reason | Guideline / Category | Status |
|---|------|-------------|--------|---------------------|--------|
[one row per finding attempted in THIS iteration from accumulated-findings where iteration == current]
```

Column definitions:
- **#** — Sequential number within this iteration
- **File** — `file:line`
- **What Changed** — Brief description of the fix applied or attempted
- **Reason** — Why the change was needed (the issue/problem)
- **Guideline / Category** — The specific project guideline violated (or "General: bug/security/contract quality" for non-guideline findings), plus the category (Bug, Security, Guideline Violation, Code Quality, Test Coverage Gap, Contract Quality)
- **Status** — `fixed`, `reverted — test failure`, `reverted — attempt 2`, or `persistent — fix failed`

For condition 4 (continue), after presenting the iteration report also show the progress summary: "Iteration [N] of up to 8 — [total-fixed] findings fixed so far, [total-reverted] reverted. Starting next pass..." If the **next** iteration will be 3 or higher, append to the progress summary: "Note: context is accumulating — if output quality degrades, consider finishing remaining findings in a fresh conversation." Then increment `iteration-count` and **return to Step 5** for the next analysis pass. When returning to Step 5, re-gather the current diff (the codebase has changed due to applied fixes) and focus agents on files that had findings in any previous iteration plus any newly modified files.

### Consolidated report

After the loop ends (by convergence, termination, or cap), present the consolidated report in two parts.

**Part 1 — Cumulative summary table:**

```
## Code Review — Deep Mode Cumulative Report

**Summary:**
- Total iterations: [N]
- Total findings fixed: [N]
- Total findings reverted (test failures): [N]
- Total findings persistent (fix failed): [N]
- Final test status: pass / fail / not available

**All Changes:**

| # | Iter | File | What Changed | Reason | Guideline / Category | Status |
|---|------|------|-------------|--------|---------------------|--------|
[one row per finding from accumulated-findings, across all iterations, ordered by iteration then sequence]
```

Column definitions match the per-iteration report table, plus:
- **Iter** — Which iteration discovered/attempted this finding

The summary statistics provide a quick overview; the detailed table provides full auditability of every change attempted across all iterations.

**Part 2 — Detailed findings:**

After the cumulative table, present ALL `accumulated-findings` using the same detailed output format from Step 7 (with Summary block, Change Summary, and individual Findings with code snippets). Add these fields to the Summary block:

```
- Total iterations: [N]
- Total findings fixed: [N]
- Total findings reverted (test failures): [N]
- Total findings persistent (fix failed): [N]
```

Mark each finding's status: "(fixed)", "(reverted — test failure)", "(reverted — attempt 2)", or "(persistent — fix failed)".

## Important

- Never modify files, commit, push, or post comments without explicit user approval (deep mode has explicit approval via the confirmation step in Step 2 — all changes remain as local modifications for the user to review with `git diff` before committing)
- This skill is read-only by default — it only analyzes and reports
- When changes are too broad for effective review, recommend narrowing scope

After the review is complete, recommend the next step based on the outcome:
- If issues were found and fixed → `/optimus:commit` to commit the fixes
- If deep mode was used → `/optimus:commit` to commit the accumulated fixes, then consider `/optimus:unit-test` to strengthen test coverage
- If no issues or user skipped fixes → `/optimus:pr` to create a pull request (skip this if already reviewing a PR/MR)

Tell the user:

- **Tip:** for best results, start a fresh conversation for the next skill — each skill gathers its own context from scratch.
- **Tip (normal mode only):** Single-pass review can miss issues due to LLM attention limits. Run `/optimus:code-review deep` to iterate automatically — it fixes, tests, and repeats until clean (max 8 passes). Requires a test command in `.claude/CLAUDE.md`.
