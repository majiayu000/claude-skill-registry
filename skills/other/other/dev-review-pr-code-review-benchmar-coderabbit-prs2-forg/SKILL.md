---
name: dev-review-pr
description: Handle automated PR review feedback and merge when ready
argument-hint: "[pr-number]"
disable-model-invocation: false
---

Check GitHub Actions status, review feedback from automated reviewers (Code Rabbit,
Claude), implement or respond to feedback, and merge the PR when all feedback is
resolved.

> **MANDATORY: Run `/dev-local-review` before every commit and push.**
> This applies to step 5 (commit and push fixes) and any other commit made
> during this workflow. Do NOT push code that has not passed a local review.
> Skipping this step wastes a GitHub review round on issues that could have
> been caught locally for free.

The user provides:

- **PR number**: the pull request number to review (optional - infers from current branch)

## Workflow

### 1. Check GitHub Actions status

Use `gh pr checks <pr-number>` to see if automated reviews are complete.

**Important:** This command returns exit code 8 if any checks are pending, and
outputs them to stderr. Handle both stdout and stderr to capture all check
statuses. Output format: `check-name  status  duration  url`

**If any checks are still running (pending):**

- Report which checks are pending
- Exit with message: "GitHub Actions still running. Run this skill again when checks complete."
- DO NOT sleep or wait — let the user run the skill again later

**If checks failed:**

- Report which checks failed
- Show the failure URL from the output
- **If markdown linting failed**, offer to run it locally and fix issues (see step 1.5)
- Otherwise exit and ask user to investigate

**If all checks passed:**

- Proceed to step 2 (fetch review comments)

### 1.5. Fix markdown linting failures (if needed)

If the "Markdown Lint" check failed:

1. **Run locally to see errors:**

   ```bash
   npx markdownlint-cli2 "**/*.md"
   ```

2. **Attempt auto-fix:**

   ```bash
   npx markdownlint-cli2 --fix "**/*.md"
   ```

3. **Manually fix remaining errors** (especially MD040 - missing language tags)

4. **Verify all errors resolved:**

   ```bash
   npx markdownlint-cli2 "**/*.md"
   ```

5. **Commit and push fixes:**

   ```bash
   git add <fixed-files>
   git commit -m "Fix markdown linting errors

   Co-Authored-By: Claude <noreply@anthropic.com>"
   git push
   ```

6. **Exit and wait for checks to re-run** — user should invoke `/dev-review-pr` again after checks pass

### 1.7. Check CodeRabbit review status

CodeRabbit is configured to **auto-pause after the first reviewed commit**
(`reviews.auto_review.auto_pause_after_reviewed_commits: 1` in `.coderabbit.yaml`). This means
after every push, CodeRabbit reviews once and then pauses. The "Reviews paused"
banner in the PR comment is **normal and expected** — it does NOT mean something
went wrong or that the review is missing.

**Key insight:** CodeRabbit completes its review *before* pausing. The review
comments and review body are already available.

**How to check:**

Look at the CodeRabbit check status from step 1:

- If CodeRabbit shows `pass` — the review is done. **Proceed directly to
  step 2** to fetch the review comments. Ignore the "Reviews paused"
  banner — it just means future commits won't be auto-reviewed.
- If CodeRabbit shows `pending` or no CodeRabbit check yet — the review
  hasn't started or is still running. Exit and ask the user to re-run later.

**After implementing feedback and pushing fixes (step 5):**

Since auto-pause is on, CodeRabbit will NOT automatically review the new
commit. Post a single comment to request a fresh review:

```bash
gh pr comment <pr-number> --body "@coderabbitai review"
```

Do NOT post `@coderabbitai resume` — we *want* it to stay paused
after each review to avoid review thrashing from rapid commits.

**If CodeRabbit shows "Currently processing new changes":**

- The review is actively running. Exit and tell the user to re-run later.
- Do NOT fetch review comments yet — they may be incomplete.

#### 1.7a. Detect clean re-review (no actionable comments)

After CodeRabbit re-reviews a fix commit, it sometimes finds nothing new to
flag. When this happens, CodeRabbit does **not** post an `APPROVED` review.
Instead, it posts an **issue comment** (not a review comment) containing:

> No actionable comments were generated in the recent review.

The review state from step 6 may still show `CHANGES_REQUESTED` or
`COMMENTED` from a previous round — that's stale and misleading.

**How to detect:**

```bash
# Get the latest "no actionable comments" timestamp
NO_ACTION_TS=$(gh api repos/{owner}/{repo}/issues/{pr-number}/comments --paginate \
  | jq -r -s '(add // []) | map(select(.user.login == "coderabbitai[bot]"
    and (.body | contains("No actionable comments"))))
    | sort_by(.created_at) | last | .created_at // empty')

# Get the latest CHANGES_REQUESTED or COMMENTED review timestamp
LAST_REVIEW_TS=$(gh api repos/{owner}/{repo}/pulls/{pr-number}/reviews --paginate \
  | jq -r -s '(add // []) | map(select(.user.login == "coderabbitai[bot]"
    and (.state == "CHANGES_REQUESTED" or .state == "COMMENTED")))
    | sort_by(.submitted_at) | last | .submitted_at // empty')

# Compare timestamps (lexicographic works for ISO 8601 dates)
if [[ -z "$NO_ACTION_TS" ]]; then
  echo "No 'no actionable comments' signal found"
elif [[ -z "$LAST_REVIEW_TS" || "$NO_ACTION_TS" > "$LAST_REVIEW_TS" ]]; then
  echo "Clean re-review detected — proceeding to step 6b"
else
  echo "Review feedback still pending"
fi
```

If the "no actionable comments" comment is **newer** than the last review
with feedback, CodeRabbit is satisfied.

**When detected, skip straight to step 6b** (pre-merge branch update and
resolve). Do not loop back to step 2 looking for feedback that does not
exist.

### 2. Fetch review comments

**Important:** Inline review comments (the "tasks" users see in the GitHub UI)
are NOT returned by `gh pr view --json comments`. You must use the API directly:

```bash
gh api repos/{owner}/{repo}/pulls/{pr-number}/comments
```

This returns an array of review comment objects with:

- `path` — file path
- `line` / `start_line` — line numbers
- `body` — comment body (markdown, may include severity, suggestions)
- `html_url` — link to view the conversation
- `user.login` — reviewer (e.g., "coderabbitai[bot]", "claude-code[bot]")

**CodeRabbit comment format:**

- Body starts with severity: `_⚠️ Potential issue_ | _🟠 Major_`, `_🟡 Minor_`, or other markers
- Includes suggested fixes in `<details><summary>Suggested fix</summary>` blocks
- May include committable suggestions between `<!-- suggestion_start -->` markers
- **Important:** CodeRabbit may leave nitpick/style comments alongside major issues—fetch ALL comments, not just the first few

Parse and categorize feedback by:

- Severity (🟠 Major, 🟡 Minor, nitpick/style)
- File and line number
- Reviewer (CodeRabbit, Claude, human)

**Present ALL comments to the user** sorted by severity (Major → Minor → Nitpick) so security/critical issues are addressed first.

#### 2a. Correctly identify which comments belong to the latest review round

**CRITICAL — this is the #1 cause of missed feedback.** Do NOT filter comments
by `original_commit_id` to find "new" comments. CodeRabbit posts comments
against various commit SHAs depending on diff positioning, and a comment on
commit A may actually be new feedback triggered by commit B's review.

**The correct approach: use the review ID, not the commit ID.**

1. First, fetch all reviews and find the latest CodeRabbit review:

   ```bash
   REVIEW_ID=$(gh api --paginate repos/{owner}/{repo}/pulls/{pr-number}/reviews \
     | jq -s 'add | map(select(.user.login == "coderabbitai[bot]"))
              | sort_by(.submitted_at) | last | .id')
   echo "Latest CodeRabbit review: $REVIEW_ID"
   ```

2. Then, fetch comments and match them to reviews by `pull_request_review_id`:

   ```bash
   gh api --paginate repos/{owner}/{repo}/pulls/{pr-number}/comments \
     | jq -s --argjson rid "$REVIEW_ID" \
       'add | map(select(.pull_request_review_id == $rid))
            | map({id, path, line, body: .body[:200]})'
   ```

3. Comments from the latest review are the **new** comments for this round.
   Comments from earlier reviews that were NOT auto-resolved are **carried
   forward** and still need action.

**Why `original_commit_id` filtering is wrong:**

- CodeRabbit may post a comment against commit X even when reviewing commit Y
  (if the code at that location hasn't changed between commits)
- A single review round can produce comments with different `original_commit_id`
  values
- Filtering by the latest commit SHA misses comments CodeRabbit posted against
  older commit positions — this causes the agent to report "only 1 new comment"
  when there are actually 7

**Alternative quick approach:** If you don't want to join on review IDs, simply
fetch ALL CodeRabbit comments, exclude those that have a human reply dismissing
them (user said "out of scope"), and present the rest grouped by file. Let the
user decide which are new vs. already handled.

#### 2b. Check review bodies for duplicate and nitpick comments

**Critical:** CodeRabbit embeds additional feedback directly in **review
bodies** — not as separate inline comment threads. These appear in collapsible
sections titled "Duplicate comments" and "Nitpick comments" within the review.
They do NOT create their own threads, so they will be missed if you only fetch
inline comments.

Fetch review bodies from CodeRabbit:

```bash
gh api --paginate repos/{owner}/{repo}/pulls/{pr-number}/reviews \
  | jq -s 'add
    | map(select(.user.login == "coderabbitai[bot]"))
    | sort_by(.submitted_at)
    | map({id: .id, state: .state, body: .body, date: .submitted_at})'
```

**Look for these sections in the review body:**

- `♻️ Duplicate comments` — Issues raised previously that CodeRabbit still
  considers unresolved after re-review. These are NOT resolved just because
  the original thread was addressed — CodeRabbit is saying the fix was
  incomplete or the issue persists. **Treat these as active feedback.**
- `🧹 Nitpick comments` — Low-severity suggestions that didn't warrant a
  blocking review thread. Still present them to the user.

**For each duplicate/nitpick comment found:**

- Extract the file path, line numbers, severity, and description
- Include the suggested patch if present
- Add it to the feedback summary alongside inline comments
- **Do not dismiss duplicate comments** — they indicate CodeRabbit re-reviewed
  and still found the issue. The fix from the previous round was likely
  incomplete.

**When a review body contains duplicate comments but no new inline threads:**

- The review state will be `COMMENTED` (not `CHANGES_REQUESTED`)
- The inline comment threads from the previous round may be auto-resolved
- But the duplicate section means there is still work to do — do NOT skip
  to the merge step just because all threads show as resolved

### 3. Present feedback summary and classify into themes

**Sort comments by severity:** Major → Minor → Nitpick/Style, so critical
issues (especially security) are addressed first.

Show the user the raw feedback list, then **group comments into themes**.
A theme is a class of issue that may have multiple instances across the
codebase. Examples:

| Raw comments | Theme |
|---|---|
| "Docs say circles but widget draws rectangles" × 3 files | Doc/code mismatch: shape description |
| "No error check after fclose" in writer A | Unchecked I/O pattern |
| "No error check after fclose" in writer B | (same theme) |
| "Test only checks return value, not side effects" × 4 tests | Weak test assertions |
| "Division by zero if rect width is 0" | Missing zero-guard pattern |
| "fabsf() should be SDL_fabsf()" × 5 files | Bare C stdlib calls (portability) |

```text
## PR Review Feedback Summary

### Pending conversations: X (grouped into Y themes)

**Theme 1: [description] (N comments, severity)**
- file.c:123 — [specific instance]
- file.c:456 — [specific instance]
- README.md:78 — [specific instance]

**Theme 2: [description] (N comments, severity)**
- ...

### Resolved conversations: Z
```

If no pending conversations, skip to step 6.

### 4. Build a verification plan (CRITICAL — do not skip)

**This is the step that prevents 10+ round feedback loops.** Before touching
any code, build a comprehensive plan for each theme. The goal: fix every
instance in one pass so CodeRabbit sees zero duplicates on re-review.

#### 4a. For each theme, run an impact analysis

For each theme, **before writing any fix**, spawn an analysis agent
(`subagent_type: "Explore"`) to answer:

1. **Where else does this pattern appear?** Search all files changed in this
   PR for the same class of issue — not just the line CodeRabbit flagged.
   Use grep/glob to find every instance.

   Examples of what "same pattern" means:
   - CodeRabbit says "docs say circles" → grep for "circle" in all `.md`,
     `.h`, and `.c` files touched by this PR
   - CodeRabbit says "unchecked fclose" → grep for every `fclose` call in
     the file and check if any are unchecked
   - CodeRabbit says "test only checks return value" → check ALL similar
     tests for the same weakness, not just the one cited
   - CodeRabbit says "division by zero if width is 0" → find ALL divisions
     by width, height, or any user-derived value in the function
   - CodeRabbit says "fabsf() should be SDL_fabsf()" → grep for ALL bare
     C stdlib calls (`fabsf`, `sinf`, `cosf`, `sqrtf`, `memset`, `memcpy`,
     `strcmp`, `strlen`, `malloc`, `free`) across every `.c` and `.h` file
     in the PR — this is a critical cross-platform portability issue

2. **What documentation describes this code?** Identify every README,
   API doc, header comment, and inline comment that references the behavior
   being changed. These MUST be updated when the code changes.

3. **What tests cover this code?** Identify existing tests. If the fix
   changes behavior, those tests must be updated. If no test exists, one
   must be written.

4. **Why did we get this wrong?** Understanding the root cause prevents
   adjacent bugs:
   - Copy-paste without adaptation → check all copies
   - Misunderstanding an API → check all uses of that API
   - Missing a case in a switch/if chain → check the full chain
   - Generated code from a template → check all generated instances

#### 4b. Write the verification plan

For each theme, produce a checklist:

```text
Theme: "Radio button shape — docs say circles, code draws rectangles"
Root cause: Copy-pasted checkbox description without adapting for radio buttons

Code fixes:
  [ ] common/ui/forge_ui.h:234 — change "circle" to "rectangle" in header doc
  [ ] common/ui/README.md:89 — update radio button description
  [ ] lessons/ui/15-editable-controls/README.md:156 — fix shape description
  [ ] OR: actually make radio buttons round in forge_ui_ctx_radio()

Doc sync:
  [ ] Verify all 3 doc locations match after fix
  [ ] Check if any diagram shows radio buttons (update if so)

Tests:
  [ ] Add test asserting radio button geometry is rectangular (or round)
  [ ] Verify existing radio button tests still pass

Grep verification:
  [ ] grep -r "circle" across all files in this PR — zero false matches remain
```

**Present the full plan to the user** before executing. The user may spot
things the analysis missed or may prefer a different approach (e.g. "just
make it round" vs "fix all the docs").

#### 4c. Execute the plan with a team

For each theme that the user approves, spawn agents **in parallel** to
handle the three concerns simultaneously:

1. **Code agent** (`subagent_type: "coder"`, `run_in_background: true`) —
   Fix the code issue across ALL instances found in the impact analysis.
   Not just the line CodeRabbit pointed at — every instance of the pattern.

2. **Test agent** (`subagent_type: "tester"`, `run_in_background: true`) —
   Write or update tests for the fix. For library changes in `common/`,
   this is mandatory. The test should:
   - Verify the fix works (positive case)
   - Verify edge cases (zero values, NULL, overflow)
   - Verify the old bug does not regress

3. **Doc agent** (`subagent_type: "coder"`, `run_in_background: true`) —
   Update ALL documentation that describes the changed behavior:
   - README sections ("What you'll learn", "Key concepts", code examples)
   - API reference docs in `common/*/README.md`
   - Header comments and inline comments in `.h` files
   - Diagram descriptions if applicable

**All three agents work from the same verification plan.** Give each agent
the full plan so they understand the scope, but assign them their specific
section (code, tests, docs).

**After all agents complete**, review their changes together. Check:

- Do the doc changes match the code changes?
- Do the tests actually test the fix?
- Did any agent's changes conflict with another's?

#### 4d. Cross-verify before committing

After all theme fixes are applied, run a final verification:

1. **Grep check**: For each theme, re-run the grep queries from the impact
   analysis. Every instance should be resolved. If any remain, fix them
   before proceeding.

2. **Build check**: Build the project to catch compile errors.

   ```bash
   cmake --build build 2>&1 | tail -20
   ```

3. **Test check**: Run relevant tests to catch regressions.

   ```bash
   ctest --test-dir build -R <relevant-test>    # C tests
   pytest tests/pipeline/ -v                     # Python tests (if applicable)
   ```

4. **Doc consistency check**: For each file pair (code + doc), verify the
   doc accurately describes the current code behavior. Read both files and
   confirm they agree.

5. **Markdown lint**:

   ```bash
   npx markdownlint-cli2 "**/*.md"
   ```

6. **Python lint** (if Python files changed):

   ```bash
   ruff check && ruff format --check
   ```

If any check fails, fix the issue before proceeding. Do NOT push code that
fails tests or lint.

#### 4e. Run local review before committing (MANDATORY — DO NOT SKIP)

> **STOP. You MUST run `/dev-local-review` here.** This is not optional.
> If you skip this step, the push will contain avoidable issues that
> waste a GitHub review round. No exceptions.

After all cross-verification checks pass, run `/dev-local-review` to catch
any issues the theme-based fixes may have introduced. This is a mandatory
gate — do NOT proceed to step 5 (commit and push) until the local review
completes with zero findings.

This prevents burning a GitHub review round on issues that could have been
caught locally for free. The local review loop follows its own strict rules
(see `/dev-local-review` skill) — it must run until zero findings or until
the user explicitly agrees to stop.

### 5. Commit, push, and request re-review

After ALL themes are resolved and ALL checks pass:

1. **Stage all changed files** by explicit name (never `git add -A`):

   ```bash
   git add <file1> <file2> ...
   ```

2. **Create a single commit** summarizing all fixes:

   ```bash
   git commit -m "$(cat <<'EOF'
   Address PR feedback: [summary]

   Themes addressed:
   - [Theme 1]: [what was fixed, how many instances]
   - [Theme 2]: [what was fixed, how many instances]

   Verification:
   - All instances found via grep — none remaining
   - Tests added/updated for each fix
   - Documentation synced with code changes
   - Build and tests pass

   Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
   EOF
   )"
   ```

3. **Push once** to the PR branch:

   ```bash
   git push
   ```

4. **Request CodeRabbit re-review**:

   ```bash
   gh pr comment <pr-number> --body "@coderabbitai review"
   ```

   Do NOT use `@coderabbitai resume` — we want auto-pause to stay active.

5. **Exit** with: "Changes pushed. Run this skill again after checks
   complete."

**On next run after CodeRabbit re-reviews:**

- Check if comments are auto-resolved (CodeRabbit detects implemented fixes)
- If duplicates appear AGAIN, the fix was still incomplete. Go back to step
  4a and do a deeper analysis — do not just patch the specific line again.
- If still unresolved after implementing the suggested fix:
  - Mention CodeRabbit in a comment: "@coderabbitai I've implemented your
    suggestion in commit ABC123. Can you verify and resolve this
    conversation?"
  - OR if CodeRabbit's check is complete (not currently running):
    "@coderabbitai Why hasn't this been auto-resolved? Is there an issue
    with my implementation?"
  - If CodeRabbit is still checking: wait for it to finish before asking

### 5.5. Escalation: 3+ review rounds on the same theme

If the same theme has appeared as a duplicate comment in 3 or more review
rounds, the point-fix approach has failed. Escalate:

1. **Stop fixing symptoms.** Read the entire function or module that keeps
   getting flagged. Understand the design, not just the flagged line.

2. **Identify the root cause.** Common patterns:
   - A wrapper function and its inner function disagree on semantics
   - A layout/drawing split where both sides compute geometry independently
   - Copy-pasted code that was adapted incompletely
   - A variable declared with the wrong type, causing casts everywhere

3. **Propose a design fix** to the user. This may be a small refactor —
   extract a shared constant, change a type at its declaration, unify two
   code paths. Present it as: "This has been flagged N times because [root
   cause]. I recommend [design fix] instead of patching individual lines."

4. **Implement the design fix** with full test coverage and doc updates.
   This replaces the point-fix cycle with a single structural change.

### 6. Check if ready to merge

Check two things: the PR-level review decision AND individual reviews.

```bash
# PR-level decision (may lag behind individual reviews)
gh pr view <pr-number> --json reviewDecision,statusCheckRollup

# Individual reviews — check the LATEST review from each reviewer
gh api --paginate repos/{owner}/{repo}/pulls/{pr-number}/reviews \
  | jq -s 'add | [.[] | {user: .user.login, state: .state, date: .submitted_at}]
        | group_by(.user)
        | map(sort_by(.date) | last)'
```

**Important:** `reviewDecision` can show `CHANGES_REQUESTED` even after a
reviewer has submitted a newer `APPROVED` review. This happens because GitHub
tracks the *earliest unresolved* review, not the latest. Always check the
latest review from each reviewer — if their most recent review is `APPROVED`,
the PR is approved regardless of what `reviewDecision` says.

Verify:

- All status checks pass
- The latest review from each reviewer is `APPROVED`
- No unresolved conversations that need action

**If the latest review is `CHANGES_REQUESTED`:**

- There are blocking issues. Go back to step 2.

**If the latest review is `COMMENTED`:**

- `COMMENTED` is **not** an approval — do NOT proceed to merge.
- The reviewer left feedback (nitpicks, suggestions, or observations) that
  needs to be acknowledged before merging. Follow step 6a below.

**If the latest review is `APPROVED`:**

- All feedback is resolved. Proceed to step 7.

#### 6a. Handle COMMENTED review state

When the latest review from a reviewer is `COMMENTED`, it means they left
non-blocking feedback but did not approve. This typically happens when:

- All major issues are resolved but nitpicks remain
- CodeRabbit found minor suggestions after a re-review
- A reviewer left observations without requesting changes

**Workflow:**

1. **Read every comment** in the `COMMENTED` review (inline threads, review
   body nitpicks, and duplicate comments). Present each to the user with
   context.

2. **For each comment, ask the user:** implement the suggestion, or skip it?

3. **If the user wants to implement:** Fix the issue, commit, push, and
   request re-review (`@coderabbitai review`). Exit and wait for the next
   review round.

4. **If the user wants to skip:** Request that CodeRabbit resolve the
   conversation:

   ```bash
   gh pr comment <pr-number> --body "@coderabbitai resolve"
   ```

   This tells CodeRabbit the feedback was acknowledged and intentionally
   skipped. CodeRabbit responds with an `APPROVED` review.

5. **CRITICAL: No commits after resolve.** Any new commit on the branch
   — your own code, a merge from main, a rebase — dismisses the approval
   that `@coderabbitai resolve` grants. This forces you to start the
   cycle over.

   Also do NOT request another review (`@coderabbitai review`) — that
   triggers a new feedback round.

6. **Update the branch before requesting resolve.** Any commit after
   resolve — including a merge from main — dismisses the approval. So
   update the branch **first**, then resolve, then merge the PR.

   **Practical workflow:**

   a. Push all local changes first (if any). Wait for checks to pass.

   b. Check if the branch is behind main:

      ```bash
      gh pr view <pr-number> --json mergeStateStatus \
        --jq '.mergeStateStatus'
      ```

   c. If `BEHIND`, merge main and push **before** requesting resolve:

      ```bash
      git fetch origin main
      git merge origin/main --no-edit
      git push
      ```

      Wait for checks to pass on the updated branch. CodeRabbit's
      auto-pause prevents the main merge from triggering new review
      feedback.

   d. Once the branch is up to date and checks pass, request resolve:

      ```bash
      gh pr comment <pr-number> --body "@coderabbitai resolve"
      ```

   e. After CodeRabbit posts the `APPROVED` review, merge immediately:

      ```bash
      gh pr merge <pr-number> --squash --delete-branch
      ```

      No `--admin` needed because the branch is already up to date and
      no commits were made after the resolve.

   **Fallback — if you already resolved before updating the branch:**

   If the approval was dismissed by a main merge, use `--admin` to merge:

   ```bash
   gh pr merge <pr-number> --squash --delete-branch --admin
   ```

   Only use `--admin` when: the nitpick was intentionally skipped
   with user confirmation, all checks are green, and the only reason
   for the missing approval is the main merge dismissing it. Present
   this to the user for confirmation.

#### 6b. Pre-merge branch update and resolve

When all feedback is addressed (either via fixes or the "no actionable
comments" signal from step 1.7a), prepare the branch for merge:

1. **Check if the branch is behind main:**

   ```bash
   gh pr view <pr-number> --json mergeStateStatus \
     --jq '.mergeStateStatus'
   ```

2. **If `BEHIND`, update the branch first:**

   ```bash
   git fetch origin main
   git merge origin/main --no-edit
   git push
   ```

   Wait for all checks to pass on the updated branch. CodeRabbit's
   auto-pause prevents the main merge from triggering new review feedback.

3. **Once the branch is up to date and checks pass, request resolve:**

   ```bash
   gh pr comment <pr-number> --body "@coderabbitai resolve"
   ```

4. **After CodeRabbit posts the `APPROVED` review, proceed to step 7.**

**Why this order matters:** Any commit after `@coderabbitai resolve`
(including a merge from main) dismisses the approval. By merging main
*before* resolve, the approval sticks and you can merge the PR normally
without `--admin`.

### 7. Merge the PR

Ask user for confirmation:

```text
✅ All feedback resolved, all checks passing, PR approved.

Ready to merge PR #X: "Title"
Branch: lesson-03-uniforms-and-motion → main

Merge method:
1. Squash and merge (recommended for lessons)
2. Merge commit
3. Rebase and merge
```

After user confirmation:

```bash
gh pr merge <pr-number> --squash --delete-branch
```

Show success message with merged commit SHA.

## GitHub CLI commands reference

```bash
# Check PR status (exit code 8 if any checks are pending)
gh pr checks <pr-number>

# Get inline review comments (the "tasks" shown in GitHub UI)
# IMPORTANT: This is the correct way to fetch review feedback
gh api repos/{owner}/{repo}/pulls/{pr-number}/comments

# View PR details (does NOT include inline review comments)
gh pr view <pr-number> --json reviewDecision,statusCheckRollup

# View specific workflow run
gh run view <run-id>

# Reply to a specific review comment thread (CORRECT - creates nested reply)
# Use this to respond to CodeRabbit/Claude feedback on specific lines
# IMPORTANT: Must include PR number in path - repos/{owner}/{repo}/pulls/{pr-number}/comments/{comment-id}/replies
# Example: gh api repos/RosyGameStudio/forge-gpu/pulls/1/comments/2807683534/replies
gh api repos/{owner}/{repo}/pulls/{pr-number}/comments/{comment-id}/replies \
  -f body="response text"

# Post a general PR comment (AVOID - doesn't thread properly with review feedback)
# This creates a standalone comment, not a reply to a review thread
gh pr comment <pr-number> --body "response text"

# Ask CodeRabbit to verify/resolve after implementing a fix (reply to the comment thread)
# IMPORTANT: Must include PR number in the path (not just comment ID)
gh api repos/{owner}/{repo}/pulls/{pr-number}/comments/{comment-id}/replies \
  -f body="@coderabbitai I've implemented your suggestion in commit ABC123. Can you verify and resolve this conversation?"

# Resolve a review thread manually
# Note: GitHub CLI doesn't directly support this - may need gh api or manual UI resolution
# Usually let CodeRabbit auto-resolve when it re-reviews

# Merge PR
gh pr merge <pr-number> --squash --delete-branch
```

## The anti-pattern this skill prevents

**Fix-the-line-not-the-pattern** is the #1 cause of 10+ round review cycles.
It looks like this:

1. CodeRabbit says "docs say circles but code draws rectangles" on file A
2. Agent fixes file A. Pushes.
3. CodeRabbit says "docs say circles" on file B (same issue, different file)
4. Agent fixes file B. Pushes.
5. CodeRabbit says "docs say circles" on file C. Duplicate comment.
6. Repeat for 14 rounds.

The correct response to step 1 is: grep for "circle" across every file in
the PR, fix all of them, update all docs, add a test, and push once.

**Every piece of feedback is a signal about a class of issue, not just a
single line.** Treat it that way.

## Implementation notes

- **Never sleep or wait** — if actions are running, exit and tell user to re-run
- Can be run multiple times — each run picks up where it left off
- Commit messages for feedback changes should reference the PR number
- If Code Rabbit or Claude give conflicting advice, prioritize project conventions from CLAUDE.md
- Always show the user what will be changed before making code modifications
- Use the same commit message format as publish-lesson (with Co-Authored-By line)
- **The "X out of Y pending tasks"** shown in GitHub UI are the unresolved review comment threads—fetch them via `gh api repos/{owner}/{repo}/pulls/{pr-number}/comments`
- **CodeRabbit auto-pause is intentional:** CodeRabbit is configured to auto-pause after reviewing each commit (`reviews.auto_review.auto_pause_after_reviewed_commits: 1`). The "Reviews paused" banner is normal — it means CodeRabbit already completed its review and is waiting. Do NOT post `@coderabbitai resume` — we want it paused to prevent review thrashing. After pushing fixes, request a single fresh review with `@coderabbitai review`. If CodeRabbit shows "Currently processing new changes", wait for it to finish before fetching comments.
- **CodeRabbit auto-resolution:** CodeRabbit automatically resolves conversations when it detects the suggested fix was implemented in a new commit. Let it auto-resolve; only ask it to resolve manually if it doesn't detect your fix after re-review.
- **CodeRabbit duplicate comments:** When CodeRabbit re-reviews after a fix, it may move previously unresolved issues into a "Duplicate comments" section in the review body instead of creating new inline threads. These are NOT resolved — they indicate the fix was incomplete. Always check the latest review body for `♻️ Duplicate comments` and `🧹 Nitpick comments` sections and treat them as active feedback requiring action.
- **Reply to comment threads:** Always use `gh api repos/{owner}/{repo}/pulls/{pr-number}/comments/{comment-id}/replies` to reply to specific review comments. This keeps conversations threaded. Do NOT use `gh pr comment` for replies—it creates unthreaded general comments.
  - **Common mistake:** Forgetting to include the PR number in the path (e.g., `repos/{owner}/{repo}/pulls/comments/{id}/replies` won't work—must be `pulls/{pr-number}/comments/{id}/replies`)
- **Team execution is mandatory for non-trivial feedback.** If a theme
  touches both code and documentation, or if a theme involves library code
  in `common/`, you MUST spawn separate agents for code, tests, and docs.
  A single agent making all changes will miss the cross-cutting concerns
  that cause duplicate comments.
- **Impact analysis before code changes.** Never start editing code until
  the grep/search phase is complete. The 30 seconds spent searching saves
  hours of review round-trips.
- **Tests catch what CodeRabbit cannot.** CodeRabbit does static analysis.
  A test that exercises the actual code path will find runtime bugs (NULL
  derefs, off-by-one, division by zero) that no review tool can see. For
  library changes in `common/`, tests are non-negotiable.
- **"No actionable comments" is CodeRabbit's clean signal.** When CodeRabbit
  re-reviews and finds nothing, it posts an issue comment (not a review)
  containing "No actionable comments were generated in the recent review."
  The review state stays `COMMENTED` or `CHANGES_REQUESTED` from the
  previous round — do not wait for an `APPROVED` review that will never
  come. Detect this comment (step 1.7a) and proceed to step 6b.
- **Merge main before resolve, not after.** Any commit after
  `@coderabbitai resolve` dismisses the approval. Always update the branch
  with main *before* requesting resolve (step 6b). This avoids the catch-22
  of needing `--admin` to merge.

## Error handling

- If `gh` CLI is not installed or not authenticated, provide clear setup instructions
- If PR doesn't exist, report error
- If branch has conflicts, report and exit (user must resolve manually)
- If merge is blocked by branch protection rules, report the blocking rules

## Example interaction

```text
Running dev-review-pr for PR #224...

✓ All GitHub Actions checks passed
✓ Found 6 pending conversations

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Grouped into 3 themes:

Theme 1: Doc/code mismatch — radio button shape (3 comments, Minor)
  - common/ui/forge_ui.h:234 — header says "circle"
  - common/ui/README.md:89 — API docs say "circular"
  - lessons/ui/15-editable-controls/README.md:156 — lesson says "round"

Theme 2: Unchecked division by zero (2 comments, Major)
  - forge_ui.h:1200 — sv_rect.w can be 0
  - forge_ui.h:1240 — hue_rect.w can be 0

Theme 3: Weak test assertions (1 comment, Minor)
  - test_ui_controls.c:89 — only checks return, not side effects

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Impact analysis for Theme 1:

  grep found 5 additional instances of "circle/circular/round"
  in radio button context across the PR files:
    - forge_ui.h line 198 (function doc)
    - forge_ui.h line 892 (inline comment)
    - README.md line 34 (widget table)
    - README.md line 201 (API section)
    - SKILL.md line 45 (skill description)

  Root cause: checkbox description was copy-pasted for radio
  buttons without adapting the shape description.

  Verification plan:
    Code: fix all 8 instances (3 flagged + 5 found)
    Docs: verify all docs agree after fix
    Tests: add assertion for radio button draw data
    Grep: re-run "circle" search — expect 0 matches

[User approves plan]
[Spawns code + test + doc agents in parallel]
[All agents complete]
[Cross-verification: grep confirms 0 remaining, tests pass]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
All 3 themes resolved. Building... ✓ Tests... ✓ Lint... ✓

✓ Committed: "Address PR feedback: fix radio shape docs (8 instances),
  add zero-guards to color picker (3 divisions), strengthen test assertions
  (6 widget tests)"
✓ Pushed (single push)
✓ Requested CodeRabbit re-review

Run this skill again after checks complete.
```
