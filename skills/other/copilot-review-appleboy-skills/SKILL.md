---
name: copilot-review
description: "Runs a single Copilot review check-fix cycle on a PR using gh CLI. Use this skill whenever the user wants to: check and fix Copilot review comments, request a Copilot code review on a PR, or iterate on PR feedback. Trigger on phrases like 'copilot review', 'fix PR comments', 'iterate on PR', 're-review', or when the user mentions 'gh pr' with 'copilot'. Combine with /loop for automated repeated cycles, e.g. '/loop 2m /copilot-review'."
---

# Copilot Review

A single-pass check-fix cycle for Copilot review comments. Designed to be called repeatedly via `/loop`:

```
/loop 2m /copilot-review
```

Each invocation runs one iteration: check for unresolved comments → fix → push → resolve → re-trigger review. When no comments remain, stop the loop.

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
          path: .comments.nodes[0].path,
          line: (.comments.nodes[0].line // .comments.nodes[0].originalLine),
          comment: .comments.nodes[0].body
        }]
  }'
```

Apply the following decision logic in order:

1. **No Copilot review exists yet** — report "No Copilot review found, triggering one..." → run `gh pr edit ... --add-reviewer "@copilot"` → **stop, wait for next cycle**.
2. **`review.submittedAt` < `latestCommit`** — Copilot has not reviewed the latest push. **Report "Waiting for Copilot to review latest push..." and stop.**
3. **Parse `review.body`** — Copilot's review summary always contains a line like:
   - `"generated no new comments"` → Copilot reviewed and found nothing. Report "Copilot review passed (no new comments) — ready for human review" and **stop the loop**.
   - `"generated N comments"` (N > 0) → Copilot found issues. **Proceed to Step 3.**
   - If the body doesn't match either pattern (e.g., first overview-only review), **proceed to Step 3** to check for unresolved threads anyway.

### 3. Process unresolved Copilot review comments

The `unresolvedThreads` array from the Step 2 query already contains all unresolved threads authored by Copilot.

If `unresolvedThreads` is **empty** and `review.body` contains `"generated no new comments"`, report "All Copilot comments resolved — ready for human review" and **stop the loop**.

If `unresolvedThreads` is **empty** but `review.body` contains `"generated N comments"` (N > 0), this means all threads from that review were already resolved. **Stop the loop** — ready for human review.

If `unresolvedThreads` is **not empty**, proceed to fix each comment.

### 4. Fix the code

For each unresolved comment:

1. Read the referenced file and line.
2. Understand the suggestion — evaluate whether it makes sense in the project context.
3. Apply the fix.

**Do not blindly accept every suggestion.** Copilot may repeat already-resolved comments or suggest changes that conflict with project architecture. If a suggestion is incorrect or irrelevant, skip it and note the reason.

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

### 7. Resolve fixed threads

After pushing, resolve each thread that was successfully addressed by inlining its ID:

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

The next `/loop` cycle will check for new comments from this re-review.

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
- **Free for open-source repos.** No Copilot subscription required.
- **Add `.github/copilot-instructions.md`** to guide Copilot's review behavior (coding style, conventions, etc.).
