---
name: fetch-pr-feedback
description: Fetch unresolved review comments from a PR and evaluate with receive-feedback skill
disable-model-invocation: true
---

# Fetch PR Feedback

Fetch review comments from all reviewers on the current PR, format them, and evaluate using the receive-feedback skill. Excludes the PR author and current user by default. Line-specific comments belonging to resolved review threads are also excluded by default.

## Usage

```bash
/beagle-core:fetch-pr-feedback [--pr <number>] [--include-author] [--include-resolved]
```

**Flags:**
- `--pr <number>` - PR number to target (default: current branch's PR)
- `--include-author` - Include PR author's own comments (default: excluded)
- `--include-resolved` - Include line-specific comments from resolved review threads (default: excluded)

## Instructions

### Gates (sequence; do not skip)

Advance only after each **Pass when** is satisfied.

1. **PR context** — **Pass when:** `$PR_NUMBER` is set to a positive integer and `gh pr view` / `gh api` for that PR completed with exit code **0**, **or** you stop in **Get PR Context** with only the failure given there (“No PR found for current branch…”).
2. **Fetch** — **Pass when:** the resolved-thread GraphQL call (skipped if `--include-resolved`) and both paginated `gh api … | jq -s -f …` runs (issue comments + review comments) exit **0** and parse as JSON (empty `[]` is valid). On non-zero exit or jq error, stop; surface command stderr—do not invent comments.
3. **Formatted artifact** — **Pass when:** output is either (a) markdown matching **Format Feedback Document** (header `# PR #$PR_NUMBER Review Feedback`, per-reviewer `## Reviewer: …` with Summary / Line-Specific sections), **or** (b) exactly: `No review comments found on this PR (excluding PR author, current user, and resolved threads).`
4. **Load receive-feedback** — **Pass when:** the Skill tool successfully loads `beagle-core:receive-feedback`; only then run that skill’s verify → evaluate → execute loop on that formatted document.

### 1. Parse Arguments

Extract flags from `$ARGUMENTS`:
- `--pr <number>` or detect from current branch
- `--include-author` flag (boolean, default false)
- `--include-resolved` flag (boolean, default false)

### 2. Get PR Context

```bash
# If --pr was specified, use that number directly
# Otherwise, get PR for current branch:
gh pr view --json number,headRefName,url,author --jq '{number, headRefName, url, author: .author.login}'

# Get repo owner/name
gh repo view --json owner,name --jq '{owner: .owner.login, name: .name}'

# Get current authenticated user
gh api user --jq '.login'
```

Store as `$PR_NUMBER`, `$PR_AUTHOR`, `$OWNER`, `$REPO`, `$CURRENT_USER`.

**Note:** `$OWNER`, `$REPO`, etc. are placeholders. Substitute actual values from previous steps.

If no PR exists for current branch, fail with: "No PR found for current branch. Use `--pr` to specify a PR number."

### 3. Fetch Comments

Fetch both types of comments, excluding `$PR_AUTHOR` and `$CURRENT_USER` (unless `--include-author` is set). Use `--paginate` with `jq -s` to combine paginated JSON arrays into one.

Unless `--include-resolved` is set, first fetch the databaseIds of every review comment that belongs to a resolved review thread. Issue comments (summary/walkthrough) aren't part of review threads, so this only affects line-specific review comments.

**Resolved-thread comment IDs** (skip this block entirely when `--include-resolved` is set; set `RESOLVED_IDS='[]'` instead):

```bash
RESOLVED_IDS=$(gh api graphql \
  -F owner="$OWNER" -F repo="$REPO" -F pr="$PR_NUMBER" \
  -f query='
    query($owner: String!, $repo: String!, $pr: Int!) {
      repository(owner: $owner, name: $repo) {
        pullRequest(number: $pr) {
          reviewThreads(first: 100) {
            nodes {
              isResolved
              comments(first: 100) { nodes { databaseId } }
            }
          }
        }
      }
    }
  ' \
  --jq '[.data.repository.pullRequest.reviewThreads.nodes[]
         | select(.isResolved)
         | .comments.nodes[].databaseId
         | select(. != null)]')
```

The `first: 100` limits cover typical PRs. For very large PRs (>100 threads or >100 comments in a single thread), thread/comment-level pagination would need to be added; for now, that's a known limitation.

Write jq filters to temp files using heredocs with single-quoted delimiters (prevents shell escaping issues with `!=`, regex patterns, and angle brackets):

**Issue comments** (summary/walkthrough posts):

```bash
cat > /tmp/issue_comments.jq << 'JQEOF'
def clean_body:
  gsub("<!-- suggestion_start -->.*?<!-- suggestion_end -->"; ""; "s")
  | gsub("<!--.*?-->"; ""; "s")
  | gsub("<details>\\s*<summary>\\s*🧩 Analysis chain[\\s\\S]*?</details>"; ""; "s")
  | gsub("<details>\\s*<summary>\\s*🤖 Prompt for AI Agents[\\s\\S]*?</details>"; ""; "s")
  | gsub("<details>\\s*<summary>\\s*📝 Committable suggestion[\\s\\S]*?</details>"; ""; "s")
  | gsub("<details>\\s*<summary>Past reviewee.*?</details>"; ""; "s")
  | gsub("<details>\\s*<summary>Recent review details[\\s\\S]*?</details>"; ""; "s")
  | gsub("<details>\\s*<summary>\\s*Tips\\b.*?</details>"; ""; "s")
  | gsub("\\n?\\n---\\n+(?=\\s*(?:✨\\s*Finishing Touches|🪧\\s*Tips?|🤖\\s*Generated|<sub>|_Generated by|Generated by Claude|Generated with))[\\s\\S]*$"; ""; "s")
  | gsub("^\\s+|\\s+$"; "")
  | if length > 4000 then .[:4000] + "\n\n[comment truncated]" else . end
;
[(add // []) | .[] | select(
  .user.login != $pr_author and
  .user.login != $current_user
)] |
map({id, user: .user.login, body: (.body | clean_body), created_at})
JQEOF

gh api --paginate "repos/$OWNER/$REPO/issues/$PR_NUMBER/comments" | \
  jq -s --arg pr_author "$PR_AUTHOR" --arg current_user "$CURRENT_USER" \
  -f /tmp/issue_comments.jq
```

**Review comments** (line-specific):

```bash
cat > /tmp/review_comments.jq << 'JQEOF'
def clean_body:
  gsub("<!-- suggestion_start -->.*?<!-- suggestion_end -->"; ""; "s")
  | gsub("<!--.*?-->"; ""; "s")
  | gsub("<details>\\s*<summary>\\s*🧩 Analysis chain[\\s\\S]*?</details>"; ""; "s")
  | gsub("<details>\\s*<summary>\\s*🤖 Prompt for AI Agents[\\s\\S]*?</details>"; ""; "s")
  | gsub("<details>\\s*<summary>\\s*📝 Committable suggestion[\\s\\S]*?</details>"; ""; "s")
  | gsub("<details>\\s*<summary>Past reviewee.*?</details>"; ""; "s")
  | gsub("<details>\\s*<summary>Recent review details[\\s\\S]*?</details>"; ""; "s")
  | gsub("<details>\\s*<summary>\\s*Tips\\b.*?</details>"; ""; "s")
  | gsub("\\n?\\n---\\n+(?=\\s*(?:✨\\s*Finishing Touches|🪧\\s*Tips?|🤖\\s*Generated|<sub>|_Generated by|Generated by Claude|Generated with))[\\s\\S]*$"; ""; "s")
  | gsub("^\\s+|\\s+$"; "")
  | if length > 4000 then .[:4000] + "\n\n[comment truncated]" else . end
;
[(add // []) | .[] | select(
  .user.login != $pr_author and
  .user.login != $current_user and
  (.id as $comment_id | ($resolved_ids | index($comment_id) | not))
)] |
map({
  id,
  user: .user.login,
  path,
  line_display: (
    .line as $end | .start_line as $start |
    if $start and $start != $end then "\($start)-\($end)"
    else "\($end // .original_line)" end
  ),
  body: (.body | clean_body),
  created_at
})
JQEOF

gh api --paginate "repos/$OWNER/$REPO/pulls/$PR_NUMBER/comments" | \
  jq -s --arg pr_author "$PR_AUTHOR" --arg current_user "$CURRENT_USER" \
  --argjson resolved_ids "$RESOLVED_IDS" \
  -f /tmp/review_comments.jq
```

If `--include-author` is set, omit the `--arg pr_author` parameter and the `.user.login != $pr_author` condition from both jq filter files. Keep the `$current_user` exclusion either way. The `$resolved_ids` filter naturally becomes a no-op when `RESOLVED_IDS='[]'` (the `--include-resolved` path), so leave it in place.

### 4. Format Feedback Document

**Noise stripping** — handled by the `clean_body` jq function in Step 3. Order matters: `<!-- suggestion_start -->...<!-- suggestion_end -->` blocks are removed first, then remaining HTML comments, then known-noise `<details>` blocks (Analysis chain, Prompt for AI Agents, Committable suggestion, Past reviewee, Recent review details, Tips), and finally the `---` footer boilerplate. The `<details>` blocks must be stripped **before** the `---` footer pattern because bot analysis chains contain `---` separators that would otherwise truncate the actual finding. Substantive `<details>` blocks (e.g. "Suggested fix", "Proposed fix") are preserved. Comments exceeding 4000 chars after stripping are truncated with a `[comment truncated]` marker.

**Group by reviewer** — organize the formatted output by reviewer username:

```markdown
# PR #$PR_NUMBER Review Feedback

## Reviewer: coderabbitai[bot]

### Summary Comments
[Issue comments from this reviewer, each separated by ---]

### Line-Specific Comments
[Review comments from this reviewer, each formatted as:]

**File: `path/to/file.ts:42`**
[cleaned comment body]

---

## Reviewer: another-reviewer

### Summary Comments
...

### Line-Specific Comments
...
```

If no comments found from any reviewer, output: "No review comments found on this PR (excluding PR author, current user, and resolved threads)."

### 5. Evaluate with receive-feedback

Use the Skill tool to load the receive-feedback skill: `Skill(skill: "beagle-core:receive-feedback")`

Then process the formatted feedback document:

1. Parse each actionable item from the formatted document
2. Process each item through verify → evaluate → execute
3. Produce structured response summary

## Example

```bash
# Fetch unresolved reviewer comments on current branch's PR (default)
/beagle-core:fetch-pr-feedback

# Fetch from a specific PR
/beagle-core:fetch-pr-feedback --pr 123

# Include PR author's own comments
/beagle-core:fetch-pr-feedback --include-author

# Include line-specific comments from resolved review threads
/beagle-core:fetch-pr-feedback --include-resolved

# Combined
/beagle-core:fetch-pr-feedback --pr 456 --include-author --include-resolved
```
