---
name: copilot-review
description: "Runs a single Copilot review check-fix cycle on a PR using gh CLI. Use this skill whenever the user wants to: check and fix Copilot review comments, request a Copilot code review on a PR, or iterate on PR feedback. Trigger on phrases like 'copilot review', 'fix PR comments', 'iterate on PR', 're-review', or when the user mentions 'gh pr' with 'copilot'. Combine with /loop for automated repeated cycles, e.g. '/loop 2m /copilot-review'."
---

# Copilot Review

A single-pass check-fix cycle for Copilot review comments. Designed to be called repeatedly via `/loop`:

```
/loop 2m /copilot-review
```

Each invocation runs one iteration: check for unresolved comments → fix → push → reply with a fix report → resolve → re-trigger review. The loop terminates ONLY when Copilot's review body contains `"generated no new comments"` or `"generated 0 comment"`.

## Prerequisites

- `gh` CLI v2.88.0+
- Authenticated: `gh auth status`

---

## Steps

### 1. Detect the PR

If the user provides a PR number and repo, use those directly. Otherwise, auto-detect from the current branch:

```bash
gh pr view --json number,url,headRepository -q '
  "PR #\(.number) — \(.headRepository.owner.login)/\(.headRepository.name)\n\(.url)"
'
```

If no PR is found on the current branch, ask the user for the PR number and repo.

Extract and store:

- `OWNER` — repository owner
- `REPO` — repository name
- `PR_NUM` — pull request number

### 2. Check Copilot review status

Before acting on comments, confirm two things: (a) Copilot has finished reviewing, and (b) the review covers the latest push. Without the timing check, a common race condition occurs: after fixing and re-triggering, the next cycle sees the old review (state = COMMENTED), finds all old threads resolved, and falsely concludes "no unresolved comments" — stopping the loop before Copilot's new review arrives.

**IMPORTANT:** Use GraphQL (not `gh pr view --json reviews`) to fetch reviews. The REST API returns `author.login` as `"copilot"`, but GraphQL returns `"copilot-pull-request-reviewer"`. Using GraphQL consistently avoids mismatches.

Use a single GraphQL query to get the latest Copilot review (with body), the latest commit timestamp, and all unresolved threads:

```bash
gh api graphql -f query='
  query($owner: String!, $repo: String!, $pr: Int!) {
    repository(owner: $owner, name: $repo) {
      pullRequest(number: $pr) {
        reviews(last: 20) {
          nodes {
            author { login }
            state
            submittedAt
            body
          }
        }
        commits(last: 1) {
          nodes { commit { committedDate } }
        }
        reviewThreads(first: 100) {
          nodes {
            id
            isResolved
            comments(first: 10) {
              nodes {
                databaseId
                body
                author { login }
                path
                line
                originalLine
              }
            }
          }
        }
      }
    }
  }
' -F owner="${OWNER}" -F repo="${REPO}" -F pr="${PR_NUM}" \
  --jq '{
    review: ([.data.repository.pullRequest.reviews.nodes[]
      | select(.author.login == "copilot-pull-request-reviewer")]
      | sort_by(.submittedAt) | .[-1]
      | {state, submittedAt, body}),
    latestCommit: .data.repository.pullRequest.commits.nodes[-1].commit.committedDate,
    unresolvedThreads: [.data.repository.pullRequest.reviewThreads.nodes[]
      | select(.isResolved == false)
      | select(.comments.nodes[0].author.login == "copilot-pull-request-reviewer")
      | {
          threadId: .id,
          commentId: .comments.nodes[0].databaseId,
          path: .comments.nodes[0].path,
          line: (.comments.nodes[0].line // .comments.nodes[0].originalLine),
          comment: .comments.nodes[0].body
        }]
  }'
```

Apply the following decision logic in order:

1. **No Copilot review exists yet** — report "No Copilot review found, triggering one..." → run `gh pr edit ... --add-reviewer "@copilot"` → **return (end this cycle, wait for next `/loop` invocation).**
2. **`review.submittedAt` < `latestCommit`** — Copilot has not reviewed the latest push. **Report "Waiting for Copilot to review latest push..." and return (end this cycle; do NOT stop the loop).**
3. **`review.submittedAt` <= `lastSeenReviewAt`** — If you recorded a `lastSeenReviewAt` value from a previous cycle (Step 8), and the current `review.submittedAt` is equal to or older than that value, the re-triggered review has not arrived yet. **Report "Waiting for re-triggered Copilot review to arrive..." and return (end this cycle; do NOT stop the loop).** Do NOT reason about whether Copilot "will" or "won't" re-review. Copilot was already re-triggered in the previous cycle's Step 8 — it WILL produce a new review; it simply hasn't arrived yet. This is true even when all threads are resolved and no code was pushed. NEVER terminate the loop from this check. If `review.submittedAt` is newer than `lastSeenReviewAt`, the new review has arrived — clear `lastSeenReviewAt` and continue to check #4.
4. **Parse `review.body`** — Copilot's review summary always contains a line like:
   - `"generated no new comments"` or `"generated 0 comment"` → Copilot reviewed and found nothing. Report "Copilot review passed (no new comments) — ready for human review" and **STOP THE LOOP (terminate entirely).** This is the ONLY check that may terminate the loop.
   - `"generated N comments"` (N > 0) → Copilot found issues. **Proceed to Step 3.**
   - If the body doesn't match either pattern (e.g., first overview-only review), **proceed to Step 3** to check for unresolved threads anyway.

### 3. Process unresolved Copilot review comments

The `unresolvedThreads` array from the Step 2 query already contains all unresolved threads authored by Copilot.

If `review.body` contains `"generated no new comments"` or matches `"generated 0 comment"`, Copilot found no issues. Report "All Copilot comments resolved — ready for human review" and **stop the loop**.

If `review.body` contains `"generated N comments"` (N > 0) but `unresolvedThreads` is **empty**, this means all threads were already resolved — but Copilot may find new issues on re-review. **Do NOT stop.** Proceed to Step 7 (resolve any remaining threads) and Step 8 (re-trigger) to let Copilot confirm with a fresh review.

If `unresolvedThreads` is **not empty**, proceed to fix each comment.

### 4. Fix the code

For each unresolved comment:

1. Read the referenced file and line.
2. Understand the suggestion — evaluate whether it makes sense in the project context.
3. Apply the fix.

**Do not blindly accept every suggestion.** Copilot may repeat already-resolved comments or suggest changes that conflict with project architecture. If a suggestion is incorrect or irrelevant, skip it and note the reason.

**If no code changes were made** (all suggestions skipped as incorrect or irrelevant), skip Steps 5 and 6 — no tests to run and no commit/push needed. Proceed directly to Step 7 to resolve the evaluated threads, then Step 8 to re-trigger. Note: since no new commit is pushed in this case, `lastSeenReviewAt` tracking (Step 2 check #3) is essential so the next cycle's Check #3 will correctly return (end that cycle) while waiting for the re-triggered review, rather than proceeding with stale data. The re-triggered review WILL arrive eventually — the next cycle just needs to wait.

### 5. Run tests

Run the project's test suite before committing. A fix that breaks other things is worse than the original issue.

If tests fail:
- Diagnose and fix the test failure.
- If the fix conflicts with the Copilot suggestion, revert that suggestion and note it as skipped.
- Re-run tests until they pass.

### 6. Commit and push

Use the **commit-message** skill (`/commit-message`) to generate a proper conventional commit message for the fixes.

After committing, push the changes:

```bash
git push
```

### 7. Reply to each thread with a fix report

**Before resolving, post a reply on each addressed thread so the reviewer can see exactly what changed.** This is the audit trail — a resolved thread with no explanation forces the reviewer to diff the code to understand the fix. Reply using the thread's first-comment `commentId` (the `databaseId` from the Step 2 query):

```bash
gh api "repos/${OWNER}/${REPO}/pulls/${PR_NUM}/comments/<COMMENT_ID>/replies" \
  -f body="$(cat <<'EOF'
Fixed in dff6b1f — Keep cached JWKS keys when an unknown-kid refetch fails.

**Fix:** `internal/jwks/remote.go` (`GetKey`). Previously, a refetch triggered by an unknown `kid` overwrote the in-memory cache with the network response *before* checking the error — so a provider outage (or any non-200) wiped every still-valid key and broke verification for tokens that were perfectly fine. The fix moves the cache assignment to *after* the error check: on a failed refetch we now log and return the existing cached keys untouched, and only replace the cache when the fetch actually succeeds. This makes the cache fail-open against transient outages instead of fail-closed.
**Test:** `TestFetcher_UnknownKidKeepsCacheOnRefetchFailure`. Seeds the cache with a known-good key, then points the fetcher at a server returning 500 to simulate an outage. It calls `GetKey` with an unknown `kid` to force a refetch (which is expected to fail), and asserts (a) the call returns the refetch error AND (b) a subsequent `GetKey` for the original `kid` still resolves from cache. Without the fix, step (b) fails because the cache was clobbered — so the test pins the exact regression, not just "the happy path still works".
EOF
)"
```

Each reply MUST contain all three parts, and each must **explain**, not just label:

1. **`Fixed in <commit> — <one-line summary>.`** — use the real commit SHA from `git rev-parse --short HEAD` (or the commit that carried this fix), not a placeholder.
2. **`Fix:`** — name the file and function/symbol, then describe the actual change and **why it resolves the finding**: what the old code did wrong, what the new code does instead, and the reasoning that makes it correct. A bare file path is not enough — the reviewer should understand the fix without opening the diff.
3. **`Test:`** — name the test, then describe **what scenario it sets up, what it asserts, and why that proves the fix** (ideally: how the test fails on the old code). State the regression it pins down, not just "it tests the function".

If a suggestion was **skipped** (declined as incorrect/irrelevant), still reply with a short rationale instead of a fix report, e.g. `Skipped — this conflicts with the existing retry policy in <file>; <reason>.` Then resolve the thread in Step 7b.

### 7b. Resolve fixed threads

After replying, resolve each thread that was successfully addressed by inlining its ID:

```bash
gh api graphql -f query='
  mutation {
    resolveReviewThread(input: {threadId: "<THREAD_NODE_ID>"}) {
      thread { isResolved }
    }
  }
'
```

### 8. Re-trigger Copilot review

```bash
gh pr edit ${PR_NUM} --repo ${OWNER}/${REPO} --add-reviewer "@copilot"
```

**After re-triggering, record `lastSeenReviewAt` = the current `review.submittedAt` from this cycle's Step 2 query.** The next `/loop` cycle will use this value in Step 2 check #3 to detect whether a new review has arrived before proceeding.

---

## Usage

```
/loop 2m /copilot-review
```

Or with a specific PR:

```
/loop 2m Check Copilot review on PR #123 (owner/repo) using /copilot-review
```

---

## gh Command Reference

### Trigger Copilot Review

```bash
gh pr edit <PR_NUM> --repo <OWNER/REPO> --add-reviewer "@copilot"
```

### Fetch Copilot Review Comments (REST)

For quick inspection without thread IDs — useful for a summary view:

```bash
gh api "repos/${OWNER}/${REPO}/pulls/${PR_NUM}/comments" \
  --jq '.[] | select(.user.login | test("copilot"; "i"))
    | "### \(.path):\(.line // .original_line)\n\(.body)\n"'
```

---

## Important Notes

- **Cap at 10 iterations.** Beyond that usually signals an architectural disagreement — stop and ask the user to review manually.
- **Copilot reviews are "Comment" type** — they never Approve or Block merge.
- **Author login mismatch:** REST API returns `author.login` as `"Copilot"`, but GraphQL returns `"copilot-pull-request-reviewer"`. Always use GraphQL with exact match `== "copilot-pull-request-reviewer"` for reliable detection.
- **Review body is the source of truth** for completion: `"generated no new comments"` means Copilot is done with no issues. `"generated N comments"` means there are comments to address. Do NOT rely solely on unresolved thread count — threads from previous reviews may all be resolved while a new review hasn't arrived yet.
- **Re-trigger without new commit:** When all suggestions are skipped (no code changes, no new commit), `latestCommit` doesn't change, so the timing check (`review.submittedAt < latestCommit`) alone cannot detect a stale review. The `lastSeenReviewAt` comparison (Step 2 check #3) is the reliable mechanism for this case.
- **"Return" vs "stop the loop":** Checks #1, #2, and #3 in Step 2 use "return" to mean "end this cycle and let `/loop` call the skill again later." They NEVER terminate the loop. Only Check #4 (`"generated no new comments"` / `"generated 0 comment"`) may terminate the loop entirely. When Check #3 fires (re-triggered review hasn't arrived), do NOT combine it with observations like "all threads are resolved" or "no code was pushed" to conclude the loop should stop. Copilot will produce a new review after being re-triggered — it just takes time.
- **Only 0 comments = done:** Do NOT stop the loop just because `unresolvedThreads` is empty or because all threads are resolved. If `review.body` says "generated N comments" (N > 0), threads may have been resolved but Copilot hasn't re-reviewed yet. Only terminate the loop when Copilot explicitly reports `"generated no new comments"` or `"generated 0 comment"` in `review.body`. No other condition — not empty threads, not "no code pushed", not any combination — justifies terminating the loop.
- **Always reply before resolving.** Every addressed thread gets a reply with the fix report: the commit SHA, a `Fix:` that explains what the old code did wrong and why the new code is correct (not just a file path), and a `Test:` that describes the scenario, the assertion, and how it fails on the old code (not just a test name). The reviewer should understand the change without opening the diff. Skipped suggestions get a short rationale reply. Reply via `POST /repos/{owner}/{repo}/pulls/{pr}/comments/{comment_id}/replies` using the thread's first-comment `databaseId`.
- **Free for open-source repos.** No Copilot subscription required.
- **Add `.github/copilot-instructions.md`** to guide Copilot's review behavior (coding style, conventions, etc.).
