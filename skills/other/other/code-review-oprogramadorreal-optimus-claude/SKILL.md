---
description: This skill performs local-first code review — analyzes uncommitted changes (or PRs/MRs) against project coding guidelines using up to 6 parallel review agents (bug detection, security/logic, guideline compliance ×2, code simplification, test coverage). HIGH SIGNAL only: real bugs, logic errors, security concerns, and guideline violations.
disable-model-invocation: true
---

# Code Review

Analyze local git changes (or a PR/MR) against the project's coding guidelines, using up to 6 parallel review agents for comprehensive coverage. High-signal findings only: bugs, logic errors, security issues, guideline violations. Excludes style concerns, subjective suggestions, and linter-catchable issues.

## Step 1: Determine Review Scope

Parse arguments and detect what to review.

### Multi-repo workspace detection

Read `$CLAUDE_PLUGIN_ROOT/skills/init/references/multi-repo-detection.md` for workspace detection. If a multi-repo workspace is detected:
- Run the git commands below inside each child repo (the workspace root has no `.git/`, so git commands must target individual repos)
- For PR/MR mode, the user must specify which repo — PRs/MRs belong to individual repos
- If changed files cannot be mapped to any child repo (e.g., files at the workspace root), ask the user which repo's context to apply
- Prerequisite loading in Step 2 will resolve per-repo docs independently

### Local changes (default — no arguments)

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
- **If no local changes** → check for commits ahead of the default branch:
  - Run `git log --oneline origin/main..HEAD` (try `main`, then `master` if no remote)
  - If commits found → offer to review the branch diff
  - Also check for a PR/MR (use the same platform detection as PR mode below):
    - If GitLab: `glab mr view --output json` (ignore errors if `glab` is not installed) — if it fails, check stderr: "no open merge request" or "404" means no MR; auth or network errors → inform the user
    - If GitHub: `gh pr view --json number,state,title` (ignore errors if `gh` is not installed)
    - If platform unknown: try both, ignore all errors
  - If PR/MR found → offer to review it
- **If nothing at all** → inform the user there are no changes to review and suggest staging changes or specifying a PR

### PR mode (explicit request)

When the user says "review PR #42", passes `--pr`, `#123`, or a PR URL:

**Platform detection** — read `$CLAUDE_PLUGIN_ROOT/skills/pr/references/platform-detection.md` and use the **Platform Detection Algorithm** section (including the **Signal Conflict Resolution** rule). If platform is unknown → inform the user and ask them to specify.

**GitHub projects:**
- Verify `gh` is available by running `gh --version`. If not available, inform the user that PR review requires the GitHub CLI (`gh`) and offer to review the branch diff instead
- Use `gh pr view <N> --json state,isDraft,title,body,baseRefName,headRefName` to get PR metadata
- Use `gh pr diff <N>` to get the actual diff
- If the PR is closed or merged → warn and stop

**GitLab projects:**
- Verify `glab` is available by running `glab --version`. If not available, inform the user: "This project uses GitLab. PR/MR review requires the GitLab CLI (`glab`). You can use branch diff mode instead: `/optimus:code-review changes since origin/main`." Offer to review the branch diff as a fallback.
- Use `glab mr view <N> --output json` to get MR metadata
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

## Step 2: Verify Prerequisites and Load Project Context

### Multi-repo workspace prerequisite loading

If a multi-repo workspace was detected in Step 1, resolve prerequisites per-repo:
- Determine which repo(s) the changed files belong to (from the diff file paths gathered in Step 1)
- Load each repo's `.claude/CLAUDE.md` and `.claude/docs/` independently (not the workspace root)
- If changes span multiple repos, apply per-repo context when reviewing that repo's files

### Documentation prerequisites

Read `$CLAUDE_PLUGIN_ROOT/skills/init/references/prerequisite-check.md` and apply the prerequisite check (CLAUDE.md + coding-guidelines.md existence, fallback logic).

### Agent prerequisites

Check that these files exist:
- `.claude/agents/code-simplifier.md`
- `.claude/agents/test-guardian.md`

**If either is missing**, warn the user and recommend running `/optimus:init` to install them. Use these fallbacks so the skill can still run:
- `code-simplifier.md` missing → Agent 5 (Code Simplifier) will be skipped in Step 3; the review still covers bugs, security, and guidelines via Agents 1–4
- `test-guardian.md` missing → Agent 6 (Test Guardian) will be skipped in Step 3; test coverage gaps will not be analyzed
- Both missing → both agents skipped; only Agents 1–4 run (still provides bug, security, and guideline coverage); strongly recommend `/optimus:init` for full 6-agent review

### Load constraint docs

Read `$CLAUDE_PLUGIN_ROOT/skills/init/references/constraint-doc-loading.md` for the full document loading procedure (single project and monorepo layouts, scoping rules).

These files define the review criteria. Every guideline-related finding must be justified by what these docs establish — never impose external preferences.

### Exclude git submodules

Apply the "Submodule Exclusion" rule from `$CLAUDE_PLUGIN_ROOT/skills/init/references/constraint-doc-loading.md` — exclude submodule directories from the review.

### Context summary

Before proceeding to the review, present a brief summary:
- Docs loaded (with paths)
- Docs missing (with fallback status)
- Agents available (with skip status for missing ones)
- Project type (single project / monorepo / multi-repo workspace)

Proceed immediately to Step 3 — do not wait for user confirmation.

## Step 3: Parallel Multi-Agent Review (up to 6 agents)

4 core review agents + 2 project-level agents, all launched in parallel for maximum coverage.

Launch up to 6 `general-purpose` Agent tool calls simultaneously. Agents 1–4 always run; Agents 5–6 only run if the corresponding project agent file exists (checked in Step 2).

Each agent receives the list of changed file paths from Step 1.

Read `$CLAUDE_PLUGIN_ROOT/skills/code-review/references/agent-prompts.md` for the full prompt templates, quality bar, exclusion rules, and false positive guidance for all 6 agents.

### Agent overview

| Agent | Role | Runs when |
|-------|------|-----------|
| 1 — Bug Detector | Null access, off-by-one, race conditions, resource leaks, type mismatches | Always |
| 2 — Security & Logic | SQL injection, XSS, hardcoded secrets, missing auth, API contract violations | Always |
| 3 — Guideline Compliance A | Explicit violations of project docs with exact rule citations | Always |
| 4 — Guideline Compliance B | Same task as Agent 3 — independent review reduces false negatives | Always |
| 5 — Code Simplifier | Unnecessary complexity, naming, dead code, pattern violations | `.claude/agents/code-simplifier.md` exists |
| 6 — Test Guardian | Test coverage gaps, structural barriers to testability | `.claude/agents/test-guardian.md` exists |

Each agent: max 5 findings, structured list format. Guideline agents (3–4) are constructed dynamically based on Step 2's doc loading results (single project vs monorepo paths).

### Execution

Launch all available agents simultaneously (parallel, not sequential). Wait for all launched agents to complete before proceeding to Step 4.

**Agent availability summary**: Agents 1–4 always run (no project dependencies). Agents 5–6 depend on installed project agents. If neither project agent exists, note in the summary and recommend `/optimus:init` for full 6-agent review.

## Step 4: Validate Findings

Independently verify each finding to filter false positives. Apply the verification protocol from `$CLAUDE_PLUGIN_ROOT/skills/init/references/verification-protocol.md` — treat agent-reported findings as claims that require independent evidence, not as ground truth.

For each finding from Step 3:
1. **Context check** — read ±30 lines around the flagged location to verify the issue exists in context
2. **Intent check** — look for comments, test assertions, or established patterns that explain the code's behavior (what looks like a bug may be intentional)
3. **Pre-existing check** — verify the issue was introduced by the changes, not pre-existing in unchanged code
4. **Cross-agent consensus** — for guideline findings, check if both Agents 3 and 4 flagged the same issue (consensus = higher confidence)

Assign confidence:
- **High** — clear issue with strong evidence → keep
- **Medium** — plausible issue, some evidence → keep with note
- **Low** — uncertain, likely false positive → drop

Only findings with High or Medium confidence proceed to Step 5.

## Step 5: Consolidate and Present Findings

Merge validated findings from Steps 3–4. Deduplicate: if two agents flagged the same file and line range for the same category, keep the more detailed version. For guideline findings flagged by both Agents 3 and 4, merge into one finding and note "confirmed by independent review".

### Contradiction resolution

After deduplication, check for **cross-agent contradictions** — findings that target the same code region but recommend opposite directions (e.g., "add more validation" vs. "simplify this validation"). Keep the higher-severity finding and drop the other. When severities are equal, keep the security/correctness finding — security requirements justify proportionate complexity.

### Change Summary

Before presenting findings, write a concise summary (2–4 sentences) of what the reviewed changes accomplish. Describe the intent and effect of the changes — what was added, modified, or removed and why. Base this on the diff and the agents' analysis. This lets the user verify the review understood their changes correctly.

### Severity

- **Critical** — Bugs, security vulnerabilities, runtime failures
- **Warning** — Guideline violations, missing error handling, test coverage gaps for critical paths
- **Suggestion** — Code quality improvements, minor guideline drift, test coverage gaps for non-critical paths

### Finding cap

Maximum **10 findings** across all sources, prioritized by severity then confidence. If more issues exist, note the count (e.g., "10 of ~18 findings shown") and suggest re-running with a narrower scope — e.g., `/optimus:code-review` "focus on src/auth".

### Output format

```
## Code Review

### Summary
- Scope: [local changes / PR #N / branch diff since X]
- Files reviewed: [N]
- Lines changed: +[A] / -[R]
- Findings: [N] (Critical: [N], Warning: [N], Suggestion: [N])
- Docs used: [list of docs loaded]
- Agents: bug-detector, security-reviewer, guideline-A, guideline-B[, code-simplifier][, test-guardian]
- Verdict: CHANGES LOOK GOOD / ISSUES FOUND

### Change Summary
[2–4 sentences describing what the changes do — their intent, what was added/modified/removed, and the overall effect. Keep it factual and concise.]

### Findings

**[N]. [Finding title]** (Critical/Warning/Suggestion — [Bug/Security/Guideline/Quality/Test Gap])
- **File:** `file:line`
- **Category:** [Bug | Security | Guideline Violation | Code Quality | Test Coverage Gap]
- **Guideline:** [which project guideline, or "General: bug/security"]
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

## Step 6: Offer Actions

If the verdict is **CHANGES LOOK GOOD** (no findings), skip this step — do not present any action prompt. Go directly to the recommendation in the "Important" section below.

If the verdict is **ISSUES FOUND**, use `AskUserQuestion` to present actions. The options depend on the review mode determined in Step 1:

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

## Important

- Never modify files, commit, push, or post comments without explicit user approval
- This skill is read-only by default — it only analyzes and reports
- When changes are too broad for effective review, recommend narrowing scope

After the review is complete, recommend the next step based on the outcome:
- If issues were found and fixed → `/optimus:commit` to commit the fixes
- If no issues or user skipped fixes → `/optimus:pr` to create a pull request (skip this if already reviewing a PR/MR)

Tell the user: **Tip:** for best results, start a fresh conversation for the next skill — each skill gathers its own context from scratch.
