---
name: phx-pr-review
description: 'Address feedback left on a GitHub pull request: fetch unresolved review
  threads, make agreed Elixir/Phoenix code fixes, reply, and resolve. Use for a PR
  URL/number or reviewer comments. NOT for pre-PR review, findings triage, or CI monitoring.'
---
# PR Review Response

Inspect unresolved pull-request review threads, triage them read-only by default,
and apply only explicitly approved fixes. GitHub mutations are never implied.

## Usage

```text
/phx-pr-review 42
/phx-pr-review 42 --fix
/phx-pr-review https://github.com/owner/repo/pull/42 --bots-only
/phx-pr-review 42 --no-resolve
```

## Workflow

1. Resolve the PR number or URL. Prefer a runtime GitHub connector that returns
   thread IDs and resolved state. Otherwise use this exact `gh` 2.94-compatible
   fallback (requires `command -v gh` and `gh auth status`):

```bash
PR_INPUT="${1:?PR number or URL}"
if [[ "$PR_INPUT" =~ ^https://github.com/([^/]+)/([^/]+)/pull/([0-9]+) ]]; then
  OWNER="${BASH_REMATCH[1]}"; REPO="${BASH_REMATCH[2]}"; PR="${BASH_REMATCH[3]}"
else
  OWNER=$(gh repo view --json owner --jq '.owner.login')
  REPO=$(gh repo view --json name --jq '.name'); PR="$PR_INPUT"
fi
gh api graphql --paginate -F owner="$OWNER" -F repo="$REPO" -F pr="$PR"   -f query='query($owner: String!, $repo: String!, $pr: Int!, $endCursor: String) { repository(owner: $owner, name: $repo) { pullRequest(number: $pr) { reviewThreads(first: 100, after: $endCursor) { nodes { id isResolved isOutdated path line originalLine comments(first: 100) { totalCount nodes { id databaseId body author { login __typename } replyTo { id } } } } pageInfo { hasNextPage endCursor } } } } }'
gh api graphql --paginate -F owner="$OWNER" -F repo="$REPO" -F pr="$PR"   -f query='query($owner: String!, $repo: String!, $pr: Int!, $endCursor: String) { repository(owner: $owner, name: $repo) { pullRequest(number: $pr) { reviews(first: 100, after: $endCursor) { nodes { id state body submittedAt author { login __typename } } pageInfo { hasNextPage endCursor } } } } }'
```

   `--paginate` binds each returned `pageInfo.endCursor` to `$endCursor`. Filter
   `isResolved == false` after collecting pages. Preserve thread `id`, root
   comment `id`/`databaseId`, and `author.__typename` (not login suffixes).
   `comments(first:100)` is nested and is **not** paginated by the outer command:
   if `comments.totalCount > nodes.length`, report the thread as TRUNCATED and
   fetch every comment page with this exact query. The outer query intentionally
   omits nested `comments.pageInfo` so `gh --paginate` follows only the outer
   `reviewThreads.pageInfo` cursor:

```bash
gh api graphql --paginate -F threadId="$THREAD_ID"   -f query='query($threadId: ID!, $endCursor: String) { node(id:$threadId) { ... on PullRequestReviewThread { comments(first:100, after:$endCursor) { totalCount nodes { id databaseId body author { login __typename } replyTo { id } } pageInfo { hasNextPage endCursor } } } } }'
```

   Merge all comment pages in API order and deduplicate by GraphQL `id` (first
   occurrence wins). Block triage until every truncated thread is complete. Do
   not substitute issue comments for review threads.
2. Keep only unresolved threads, preserve API order, then group by path and line.
   With `--bots-only`, use API actor type rather than a login suffix. Show one row
   per thread with author, category, outdated state, and proposed action. Review
   summaries are separate, non-resolvable context.
3. **Gate 1 — read-only selection.** Always stop after triage for an explicit list
   of selected thread IDs. Selection authorizes inspection only. `--fix` permits
   later edits but approves nothing and never selects every thread.
4. **Gate 2 — edit approval.** For each selected thread, read current code and
   propose the exact patch. Obtain explicit edit approval before editing, or record
   `EDIT: NOT APPLICABLE` with evidence. Then show the applied diff and run the
   smallest relevant compile/test check after every code change.
5. **Gate 3 — posting approval.** Draft a reply only after verification. Outdated means location drift, **not**
   addressed: require current code/diff evidence before that disposition. Show the
   diff, evidence, and exact verified reply, then obtain a separate explicit posting
   approval before posting. Use a connector
   mutation when available, or `gh api` to reply to the root review comment. If
   posting is unsupported or fails, report `NOT POSTED` with the reason.
6. **Gate 4 — resolution approval.** First confirm the post from the API response.
   Only then request a separate resolution approval. `--no-resolve` always disables resolution, regardless of
   any other flag or approval. Use the connector or `resolveReviewThread` mutation, then
   confirm returned state. Never claim replied/resolved from a draft or intent.
7. Return `thread | action | verification | reply | resolution`, changed files,
   and precise blockers. Paginated review summaries with `CHANGES_REQUESTED` or
   an actionable non-empty body are findings even when there are zero inline
   threads; report them as non-resolvable context and never call that state clean.
   Do not commit or push.

Generic read-only workers may inspect independent threads when the runtime has
them, but named custom agents are not required and sequential same-session
processing is complete.

## Iron Laws

1. **Triage always stops for explicit thread selection** — `--fix` permits but does
   not approve edits.
2. **Never post, resolve, dismiss, commit, or push without the required approval.**
3. **Never resolve before a successful reply** and never fabricate mutation state.
4. **Never claim a fix without a shown diff and successful focused verification.**
5. **Scrutinize bot and human findings equally**; Iron Laws override suggestions.

## References

- `references/response-patterns.md` — reply templates and tone
- `references/gh-commands.md` — GitHub CLI queries and mutations
- `references/bot-triage.md` — bot review triage
