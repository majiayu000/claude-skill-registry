---
name: phx-pr-review
description: Address PR review threads on Elixir/Phoenix code — fetch unresolved threads,
  fix code, reply, and resolve each thread. Use when the user shares a PR URL or mentions
  reviewer feedback.
---

# PR Review Response

Close the review loop: fetch unresolved threads → fix → reply → resolve.
GitHub's `isResolved` is the state — re-runs are idempotent, handled
threads drop out automatically.

## Usage

```
$phx-pr-review 42                  # Triage unresolved threads on PR #42
$phx-pr-review 42 --fix            # Triage + apply approved code fixes
$phx-pr-review https://...         # Full URL also works (repo parsed from URL)
$phx-pr-review 42 --bots-only      # Triage only CI bot threads (Copilot, Codex...)
$phx-pr-review 42 --no-resolve     # Reply but leave threads open
```

## Step 1: Resolve PR + Fetch Threads

`gh pr view "$PR" --json number,title,state,baseRefName,headRefName,url,author`
(accepts number or URL; URL also yields owner/repo). Then fetch ALL review
threads with thread IDs + resolved status — REST alone cannot do this:

```bash
cat > /tmp/review_threads.graphql <<'GQL'
query($owner:String!, $repo:String!, $pr:Int!, $cursor:String) {
  repository(owner:$owner, name:$repo) {
    pullRequest(number:$pr) {
      reviewThreads(first:50, after:$cursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id isResolved isOutdated path line originalLine
          comments(first:20) { nodes {
            databaseId body createdAt
            author { login __typename } } }
        }
      }
    }
  }
}
GQL
gh api graphql --paginate -F owner="$OWNER" -F repo="$REPO" -F pr="$PR" \
  -F query=@/tmp/review_threads.graphql \
  --jq '.data.repository.pullRequest.reviewThreads.nodes[]
        | select(.isResolved == false)
        | {threadId: .id, isOutdated, path, line: (.line // .originalLine),
           firstCommentId: .comments.nodes[0].databaseId,
           author: .comments.nodes[0].author.login,
           isBot: (.comments.nodes[0].author.__typename == "Bot"),
           body: .comments.nodes[0].body}'
```

Also fetch review summaries (`gh api "repos/$OWNER/$REPO/pulls/$PR/reviews"`)
— they are NOT threads and cannot be resolved; surface `CHANGES_REQUESTED`
bodies separately. Bot detection: `__typename == "Bot"` / `user.type == "Bot"`
(the `[bot]` login suffix is NOT reliable across endpoints).

## Step 2: Triage Table

Group by file, one row per thread. With `--bots-only`, keep only `isBot` rows.

| # | file:line | author | category | proposed action |
|---|-----------|--------|----------|-----------------|

Categories: **code-change** ("should be", "use X instead") · **question**
("why", "how does") · **nitpick** ("nit:", style) · **praise** (no action) ·
**discussion** (architecture) · **bot-finding** (CI bot inline comment —
verify before accepting, many are false positives) · **outdated**
(`isOutdated: true` — line moved; default: reply "addressed in {commit}" +
resolve). Present the table and let the user greenlight threads.

## Step 3: Per-Thread Loop

For each greenlit thread:

1. Read code at `path:line`; check the suggestion against Iron Laws
2. Apply fix with a user-visible diff (only with `--fix` or explicit ok)
3. Draft reply (templates: `references/response-patterns.md`)
4. **STOP — show diff + reply, get confirmation**
5. Post reply — REST, targeting the thread's root comment:

   ```bash
   gh api --method POST \
     "repos/$OWNER/$REPO/pulls/$PR/comments/$FIRST_COMMENT_ID/replies" \
     -f body="$REPLY_TEXT"
   ```

6. Resolve the thread (skip with `--no-resolve`):

   ```bash
   gh api graphql -f query='mutation($threadId:ID!){
     resolveReviewThread(input:{threadId:$threadId}){
       thread { id isResolved } }}' -F threadId="$THREAD_ID"
   ```

Mistake recovery: `unresolveReviewThread` takes the same input shape.

## Step 4: Verify

`mix compile --warnings-as-errors && mix test` scoped to changed files.
Do NOT commit or push — leave that to the user.

## Step 5: Final Summary

Print rollup: `# | thread | action | status (replied/resolved/skipped)`.
List changed files. Optionally post a top-level conversation comment
(`gh api --method POST "repos/$OWNER/$REPO/issues/$PR/comments" -f body=...`)
with the rollup — **only on user approval**.

## Iron Laws

1. **NEVER auto-post responses** — Always show drafts and get explicit approval
2. **NEVER dismiss a review** — Only the reviewer should dismiss
3. **Iron Laws override reviewer suggestions** — If a suggestion violates an Iron Law, explain why in the reply
4. **Keep responses constructive** — Acknowledge the feedback, explain reasoning
5. **Separate fixes from responses** — Apply code changes in a distinct step
6. **NEVER resolve a thread without first posting a reply** — every resolve is preceded by a reply on that thread explaining what was done
7. **NEVER claim a fix without a shown diff** — no "should be fixed" replies without a user-visible change
8. **Bot findings get the same scrutiny as humans** — decline Iron-Law-violating bot suggestions with explanation; never bulk-resolve "bot noise" without replies

## Integration

```text
PR receives review → $phx-pr-review {number}  ← YOU ARE HERE
   ↓ fetch unresolved threads (GraphQL, paginated)
   ↓ triage table → user greenlights
   ↓ per thread: fix (diff) → reply → resolve
   ↓ verify (mix compile + test) → summary
Push changes → user handles git push
```

## Next Steps

- `$phx-plan` — if findings reveal scope gaps
- `$phx-verify` — full verification before pushing
- Re-run `$phx-pr-review` after the next review round (idempotent)

## References

- `references/response-patterns.md` — Response templates and tone
- `references/gh-commands.md` — Full gh command reference (3 comment surfaces, pagination, bot detection)
- `references/bot-triage.md` — Batch-triaging CI bot review passes
