---
name: gwt-fix-pr
description: Inspect GitHub PR for CI failures, merge conflicts, update-branch requirements, reviewer comments, change requests, and unresolved review threads. Create fix plans and implement after user approval. Reply to ALL reviewer comments with action taken or reason for not addressing, then resolve threads. Notify reviewers after fixes.
metadata:
  short-description: Fix failing GitHub PRs comprehensively
---

# Gh PR Checks Plan Fix

## Overview

Use gh to inspect PRs for:

- Failing CI checks (GitHub Actions)
- Merge conflicts
- Update Branch requirements (base branch advanced)
- Reviewer comments (review summaries, inline comments, issue comments)
- Change Requests from reviewers
- Unresolved review threads

Then propose a fix plan, implement after explicit approval, **reply to every reviewer comment** (with action taken or reason for not addressing), resolve all threads, and notify reviewers.

- Depends on the `plan` skill for drafting and approving the fix plan.

Prereq: ensure `gh` is authenticated (for example, run `gh auth login` once), then run `gh auth status` with escalated permissions (include workflow/repo scopes) so `gh` commands succeed.

## Comment Response Policy

> **No reviewer comment may be left unanswered.**

- Every unresolved review thread MUST receive a reply before being resolved.
- If the feedback was addressed: reply with what was done (e.g., "Fixed: refactored as suggested.").
- If the feedback was intentionally not addressed: reply with the reason (e.g., "Not addressed: this is intentional because the API contract requires this format.").
- The `--reply-and-resolve` argument enforces this by requiring a reply entry for every unresolved thread and rejecting empty bodies.

## Diagnosis Report Anti-Patterns

### Prohibited Language

| Prohibited | Required Alternative |
|---|---|
| "We should look into..." | "Edit `path/file.ts:42` to..." |
| "There seem to be some issues" | "3 blocking items detected" |
| "This might be causing..." | "Root cause: `<error from log>`" |
| "Consider fixing..." / "It looks like..." | "Action: Fix `<what>` in `<where>`" |
| "Various CI checks are failing" | "2 CI checks failing: `build`, `lint`" |
| "Some reviewers have concerns" | "@reviewer1 requested: `<quote>`" |
| "I'll try to fix this" | "Action: \<specific fix\>" |

### Structural Prohibitions

- Prose paragraphs for reporting — use B1/I1 item format exclusively.
- Omitting the Evidence field in any BLOCKING item.
- Combining multiple independent problems into a single item.
- Omitting file paths or line numbers when the script output contains them.

## Issue/PR Comment Formatting (must follow)

- Final comment text must not contain escaped newline literals such as `\n`.
- Use real line breaks in comment bodies. Do not rely on escaped sequences for formatting.
- Before posting (`--add-comment` or manual `gh issue/pr comment`), verify the final body does not accidentally include escaped control sequences (`\n`, `\t`).
- If a raw escape sequence must be shown for explanation, include it only inside a fenced code block and clarify it is intentional.

## Issue Progress Comment Template (required for issue-based work)

When work is tracked in GitHub Issues, progress updates must use this template:

```markdown
Progress
- ...

Done
- ...

Next
- ...
```

- Post updates at least when starting work, after meaningful progress, and when blocked/unblocked.
- In `Next`, explicitly state blockers or the immediate next action.

## Inputs

- `repo`: path inside the repo (default `.`)
- `pr`: PR number or URL (optional; defaults to current branch PR)
- `mode`: inspection mode (`checks`, `conflicts`, `reviews`, `all`)
- `required-only`: limit CI checks to required checks only (uses `gh pr checks --required`)
- `gh` authentication for the repo host

## Quick start

```bash
# Inspect all (CI, conflicts, reviews) - default mode
python3 ".claude/skills/gwt-fix-pr/scripts/inspect_pr_checks.py" --repo "." --pr "<number>"

# CI checks only
python3 ".claude/skills/gwt-fix-pr/scripts/inspect_pr_checks.py" --repo "." --pr "<number>" --mode checks

# Conflicts only
python3 ".claude/skills/gwt-fix-pr/scripts/inspect_pr_checks.py" --repo "." --pr "<number>" --mode conflicts

# Reviews only (Change Requests + Unresolved Threads)
python3 ".claude/skills/gwt-fix-pr/scripts/inspect_pr_checks.py" --repo "." --pr "<number>" --mode reviews

# JSON output
python3 ".claude/skills/gwt-fix-pr/scripts/inspect_pr_checks.py" --repo "." --pr "<number>" --json

# Required checks only (if gh supports --required)
python3 ".claude/skills/gwt-fix-pr/scripts/inspect_pr_checks.py" --repo "." --pr "<number>" --mode checks --required-only

# Reply to all unresolved threads and resolve them
python3 ".claude/skills/gwt-fix-pr/scripts/inspect_pr_checks.py" --repo "." --pr "<number>" --reply-and-resolve '[
  {"threadId":"PRRT_xxx123","body":"Fixed: refactored the method as suggested."},
  {"threadId":"PRRT_xxx456","body":"Not addressed: this is intentional because the API requires this format."}
]'

# Add a comment to notify reviewers
python3 ".claude/skills/gwt-fix-pr/scripts/inspect_pr_checks.py" --repo "." --pr "<number>" --add-comment "Fixed all issues. Please re-review."
```

## Workflow

1. **Verify gh authentication.**
   - Run `gh auth status` in the repo with escalated scopes (workflow/repo).
   - If unauthenticated, ask the user to log in before proceeding.

2. **Resolve the PR.**
   - Prefer the current branch PR: `gh pr view --json number,url`.
   - If the user provides a PR number or URL, use that directly.

3. **Inspect based on mode:**

   **Conflicts Mode (`--mode conflicts`):**
   - Check `mergeable` and `mergeStateStatus` fields.
   - If `CONFLICTING` or `DIRTY`, report conflict details.
   - If `BEHIND`, report that the base branch advanced and an Update Branch is required.
   - Suggest resolution steps: fetch base branch, merge/rebase, resolve conflicts.

   **Reviews Mode (`--mode reviews`):**
   - Fetch reviews with `CHANGES_REQUESTED` state.
   - Fetch unresolved review threads using GraphQL.
   - Fetch ALL reviewer comments (review summaries, inline review comments, issue comments) without truncation.
   - Display reviewer, comment body (full text), file path, and line number.
   - Decide if reviewer feedback requires action (any change request, unresolved thread, or reviewer comment).

   **Checks Mode (`--mode checks`):**
   - Run bundled script to inspect failing CI checks.
   - Add `--required-only` to limit output to required checks when supported.
   - Fetch GitHub Actions logs and extract failure snippets.
   - For external checks (Buildkite, etc.), report URL only.

   **All Mode (`--mode all`):**
   - Run all inspections above.

4. **Produce Diagnosis Report (mandatory format).**

   Output MUST use this exact structure:

   ```text
   ## Diagnosis Report: PR #<number>

   **Merge Verdict: BLOCKED | CLEAR**
   Blocking items: <N>

   ---

   ### BLOCKING

   #### B1. [CATEGORY] <1-line title>
   - **What:** Factual statement (no speculation)
   - **Where:** file_path:line_number / check name / branch ref
   - **Evidence:** Verbatim quote from script output
   - **Action:** Specific fix (file path, command, or code change — at least one required)
   - **Auto-fix:** Yes | No (needs confirmation)

   #### B2. [CATEGORY] <1-line title>
   ...

   ---

   ### INFORMATIONAL
   #### I1. [CATEGORY] <1-line title>
   - **What / Note**

   ---

   **Summary:** <N> blocking items to fix, <M> informational items noted.
   ```

   **Classification rules:**

   - **BLOCKING:** CONFLICTING/DIRTY merge state, BEHIND, CI failure/cancelled/timed\_out/action\_required, CHANGES\_REQUESTED, unresolved review threads
   - **INFORMATIONAL:** Comments without change requests, pending CI, outdated review threads

   **Category labels:** `CONFLICT`, `BRANCH-BEHIND`, `CI-FAILURE`, `CHANGE-REQUEST`, `UNRESOLVED-THREAD`, `REVIEW-COMMENT`

   **Auto-fix judgment:**

   - **Auto-fix: Yes** — CI-FAILURE code fixes, reviewer instructions that the LLM can address with high confidence
   - **Auto-fix: No (needs confirmation)** — CONFLICT resolution (merge/rebase), low-confidence reviewer instructions, changes requiring design decisions

   **Each CHANGE-REQUEST and each UNRESOLVED-THREAD is a separate B-item.** Do not combine multiple threads or requests into one item.

5. **Decide execution path.**
   - If ALL blocking items have `Auto-fix: Yes` → display Diagnosis Report, skip plan, proceed directly to step 6.
   - If ANY blocking item has `Auto-fix: No` → create a plan referencing B-item IDs (e.g., "Fix B1: ...", "Fix B3: ...") and request user approval for `Auto-fix: No` items before proceeding.

6. **Implement fixes.**
   - Apply the approved fixes, summarize diffs/tests.
   - After applying fixes, commit changes and push to the PR branch.
   - Verify push succeeded before proceeding to step 7.
   - **After implementing fixes, proceed to step 7 to reply and resolve ALL threads.**
   - For BRANCH-BEHIND items, see [Fix Strategies: BRANCH-BEHIND](#branch-behind).
   - For CONFLICT items, see [Fix Strategies: CONFLICT](#conflict).

7. **Reply to ALL reviewer comments and resolve threads (mandatory).**
   - **CRITICAL:** Every unresolved review thread MUST receive a reply before resolution. No thread may be silently resolved or left unaddressed.
   - For each unresolved thread, prepare a reply:
     - If addressed: describe what was done (e.g., "Fixed: refactored the method as suggested in commit abc1234.")
     - If intentionally not addressed: explain the reason (e.g., "Not addressed: this is by design because ...")
   - Use `--reply-and-resolve` with a JSON array covering ALL unresolved threads.
   - The script validates completeness and rejects the operation if any thread is missing a reply.
   - Requires `Repository Permissions > Contents: Read and Write`.
   - Resolve threads at this point (after code fix is pushed). Do not wait for CI completion to resolve threads.

8. **Notify reviewers (mandatory).**
   - With `--add-comment "message"`, post a comment to the PR.
   - Include a summary of what was fixed (list each B-item and the action taken).
   - This step is not optional — always notify reviewers after fixes are applied.

9. **Verify fix (mandatory — do not skip).**
   - Re-run the inspection script with `--mode all` (regardless of initial mode).
   - Exit code 0 → all resolved → report success to user.
   - Exit code 1 → issues remain → go back to step 4 with new output.
   - No iteration limit. Continue until all issues are resolved.
   - CI still pending/queued → poll at 30-second intervals (no timeout) until ALL checks complete.
   - Wait for ALL CI checks to complete before starting fixes (pushing resets pending checks).
   - After fix push, re-enter polling to wait for new CI run to complete.

## Loop Safety Guard

- If the **same CI check name** (e.g., `build`) fails **3 consecutive iterations**:
  1. Report to user: which check, what was tried in each iteration, what keeps failing.
  2. Ask user to choose: **continue** / **abort** / **change approach**.
  3. Only proceed after explicit user decision.
- This prevents oscillation loops where fix A breaks B and fix B breaks A.
- Different checks failing in different iterations do NOT trigger the guard (e.g., `build` fails → fixed → `lint` fails is normal progression, not oscillation).

## Fix Strategies

### BRANCH-BEHIND

- Default strategy: `git fetch origin <base> && git merge origin/<base>`
- If merge results in conflicts, switch to CONFLICT handling below.

### CONFLICT

- LLM attempts to resolve conflicts after user confirmation.
- Present conflict summary (affected files, conflict markers) and proposed resolution to the user.
- Execute resolution only after user approves.

## Bundled Resources

### scripts/inspect_pr_checks.py

Comprehensive PR inspection tool. Exits non-zero when issues remain.

**Arguments:**

| Argument | Default | Description |
|----------|---------|-------------|
| `--repo` | `.` | Path inside the target Git repository |
| `--pr` | (current) | PR number or URL |
| `--mode` | `all` | Inspection mode: `checks`, `conflicts`, `reviews`, `all` |
| `--max-lines` | 160 | Max lines for log snippets |
| `--context` | 30 | Context lines around failure markers |
| `--required-only` | false | Limit CI checks to required checks only |
| `--json` | false | Emit JSON output |
| `--reply-and-resolve` | (none) | JSON array of `{threadId, body}` to reply and resolve ALL threads |
| `--add-comment` | (none) | Add a comment to the PR |

**Exit codes:**

- `0`: No issues found
- `1`: Issues detected or error occurred

**`--reply-and-resolve` JSON format:**

```json
[
  {"threadId": "PRRT_xxx123", "body": "Fixed: refactored the method as suggested."},
  {"threadId": "PRRT_xxx456", "body": "Not addressed: this is intentional because ..."}
]
```

**Validation rules:**

- Every currently unresolved thread MUST have a corresponding entry.
- Every entry MUST have a non-empty `body`.
- If any unresolved thread is missing, the script prints the missing thread details and exits with error.

## Features

### Conflict Detection

Detects merge conflicts via `mergeable` and `mergeStateStatus` fields.

- `CONFLICTING` / `DIRTY`: Conflict detected
- `BEHIND`: Base branch advanced; Update Branch required
- `MERGEABLE` / `CLEAN`: No conflicts

### Change Request Handling

Fetches reviews with `state == "CHANGES_REQUESTED"` and displays:

- Reviewer name
- Review body
- Submission timestamp

### Reviewer Comments

Fetches ALL reviewer feedback without truncation:

- Review summaries with full comment bodies
- Inline review comments (file/line) with full comment bodies
- PR issue comments with full comment bodies
- Marks review action required if any reviewer feedback exists

### Unresolved Review Threads

Uses GraphQL to fetch threads where `isResolved == false`:

- File path and line number
- Thread ID (for reply and resolution)
- Comment author and full body
- Outdated status

### Reply and Resolve

Use `--reply-and-resolve` to reply to every unresolved thread and resolve them.

- Uses GraphQL `addPullRequestReviewThreadReply` to post a reply.
- Uses GraphQL `resolveReviewThread` to mark the thread as resolved.
- Validates that ALL unresolved threads are covered (no thread left behind).
- Rejects empty reply bodies.

**Required permissions:**

- Fine-grained PAT: `Pull requests` + `Contents: Read and Write`
- Classic PAT: `repo` scope

### Reviewer Notification

Use `--add-comment "message"` to post a summary comment to the PR after fixes.

## Output Examples

### Diagnosis Report

```text
## Diagnosis Report: PR #123

**Merge Verdict: BLOCKED**
Blocking items: 3

---

### BLOCKING

#### B1. [CI-FAILURE] TypeScript build fails
- **What:** `build` check failed with compilation error
- **Where:** `src/utils/parser.ts:42` / check: `build`
- **Evidence:** `error TS2345: Argument of type 'string' is not assignable to parameter of type 'number'.`
- **Action:** Edit `src/utils/parser.ts:42` — change `parseInt(value)` to pass the correct type
- **Auto-fix:** Yes

#### B2. [CHANGE-REQUEST] @reviewer1 requests error handling
- **What:** Reviewer requested try-catch around API call
- **Where:** `src/api/client.ts:88`
- **Evidence:** "@reviewer1: Please wrap this fetch call in a try-catch block to handle network errors gracefully."
- **Action:** Add try-catch in `src/api/client.ts:88` around the `fetch()` call
- **Auto-fix:** Yes

#### B3. [CONFLICT] Merge conflict with main
- **What:** 2 files have merge conflicts
- **Where:** `src/config.ts`, `src/index.ts` / branch: `main`
- **Evidence:** `Mergeable: CONFLICTING, Merge State: DIRTY`
- **Action:** Merge `origin/main` and resolve conflicts in listed files
- **Auto-fix:** No (needs confirmation)

---

### INFORMATIONAL
#### I1. [REVIEW-COMMENT] Code style suggestion
- **What / Note:** @reviewer2 suggested extracting a helper function — non-blocking style preference

---

**Summary:** 3 blocking items to fix, 1 informational item noted.
```

### Text Output

```text
PR #123: Comprehensive Check Results
============================================================

MERGE STATUS
------------------------------------------------------------
Mergeable: CONFLICTING
Merge State: DIRTY
Base: main <- Head: feature/my-branch
Action Required: Resolve conflicts before merging

CHANGE REQUESTS
------------------------------------------------------------
From @reviewer1 (2025-01-15):
  "Please fix these issues..."

UNRESOLVED REVIEW THREADS
------------------------------------------------------------
[1] src/main.ts:42
    Thread ID: PRRT_xxx123
    @reviewer1: This needs refactoring because the current
    implementation violates the single responsibility principle.

[2] src/utils.ts:15
    Thread ID: PRRT_xxx456
    @reviewer2: Consider using a more descriptive variable name here.

CI FAILURES
------------------------------------------------------------
Check: build
Details: https://github.com/...
Failure snippet:
  Error: TypeScript compilation failed
  ...
============================================================
```

### Reply and Resolve Output

```text
OK: PRRT_xxx123 (src/main.ts:42)
OK: PRRT_xxx456 (src/utils.ts:15)

Result: 2 resolved, 0 failed, 2 total
```

### JSON Output

```json
{
  "pr": "123",
  "conflicts": {
    "hasConflicts": true,
    "mergeable": "CONFLICTING",
    "mergeStateStatus": "DIRTY",
    "baseRefName": "main",
    "headRefName": "feature/my-branch"
  },
  "changeRequests": [
    {
      "id": 123456,
      "reviewer": "reviewer1",
      "body": "Please fix these issues...",
      "submittedAt": "2025-01-15T12:00:00Z"
    }
  ],
  "unresolvedThreads": [
    {
      "id": "PRRT_xxx123",
      "path": "src/main.ts",
      "line": 42,
      "comments": [
        {"author": "reviewer1", "body": "This needs refactoring because..."}
      ]
    }
  ],
  "ciFailures": [
    {
      "name": "build",
      "status": "ok",
      "logSnippet": "..."
    }
  ]
}
```
