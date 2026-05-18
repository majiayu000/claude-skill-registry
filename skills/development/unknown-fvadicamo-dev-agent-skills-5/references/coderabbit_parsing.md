# CodeRabbit review parsing

Guide for extracting and processing all comment types from CodeRabbit PR reviews.

## Review body structure

CodeRabbit posts a single PR-level review (via `pulls/$PR/reviews` API) containing multiple sections as collapsible `<details>` blocks. The body follows this structure:

```
Actionable comments posted: N

> [!CAUTION]
> Some comments are outside the diff and can't be posted inline...

<details>
<summary>⚠️ Outside diff range comments (N)</summary>
  (actionable comments on code outside the PR diff)
</details>

<details>
<summary>♻️ Duplicate comments (N)</summary>
  (issues already flagged in a previous review)
</details>

<details>
<summary>🟡 Minor comments (N)</summary>
  (lower severity comments grouped to reduce inline noise)
</details>

<details>
<summary>🧹 Nitpick comments (N)</summary>
  (style/convention issues, lowest priority)
</details>

<details>
<summary>🤖 Prompt for all review comments with AI agents</summary>
  (global prompt covering all comments in this review)
</details>

<!-- Informational sections (not actionable, ignore): -->
<details><summary>ℹ️ Review info</summary></details>
<details><summary>⚙️ Run configuration</summary></details>
<details><summary>📥 Commits</summary></details>
<details><summary>⛔ Files ignored due to path filters (N)</summary></details>
<details><summary>📒 Files selected for processing (N)</summary></details>
<details><summary>🚧 Files skipped from review as they are similar to previous changes (N)</summary></details>
```

Not all sections are always present. CodeRabbit only includes sections that have comments. Other severity-based sections (e.g., "🔴 Critical comments", "🟠 Major comments") may also appear.

## Fetching CodeRabbit reviews

```bash
REPO=$(gh repo view --json nameWithOwner -q '.nameWithOwner')
PR=$(gh pr view --json number -q '.number')

# Get all CodeRabbit review bodies (may be multiple reviews across pushes)
gh api repos/$REPO/pulls/$PR/reviews?per_page=100 --jq '
  [.[] | select(.user.login | startswith("coderabbitai")) |
   {id, submitted_at, body}]
'
```

The `id` field is the review ID (visible in the GitHub URL as `#pullrequestreview-<id>`). Use this as the stable identifier for tracking.

## Parsing sections from the body

Each section is a `<details>` block. Extract them by matching the summary text:

| Summary pattern | Comment type | Default severity |
|----------------|--------------|-----------------|
| `⚠️ Outside diff range comments` | Code outside the PR diff | Use per-comment severity |
| `♻️ Duplicate comments` | Already flagged in previous reviews | Use per-comment severity |
| `🟡 Minor comments` | Lower severity, grouped to reduce noise | MEDIUM/LOW (use per-comment) |
| `🧹 Nitpick comments` | Style/convention issues | LOW |
| `🤖 Prompt for all review comments with AI agents` | Global AI context prompt | N/A (not a comment) |

Other severity-based sections like "🔴 Critical comments" or "🟠 Major comments" may appear. Treat any unrecognized `<details>` section with comments as actionable and classify by per-comment severity.

Informational sections (`ℹ️ Review info`, `⚙️ Run configuration`, `📥 Commits`, `⛔ Files ignored due to path filters`, `📒 Files selected for processing`, `🚧 Files skipped from review as they are similar to previous changes`) are not actionable. Ignore them.

### Per-comment structure inside sections

Each file group is wrapped in a `<details>` block. The summary format varies:

```
<!-- Outside diff / Duplicate sections: file path + count -->
<details>
<summary>file/path.ext (N)</summary>

<!-- Minor / Nitpick sections: file path + line range + count -->
<details>
<summary>file/path.ext-X-Y (N)</summary>
```

Inside each file group, individual comments follow this pattern:

```
`X-Y`: _<emoji> <type>_ | _<color> <severity>_

**Title text**

Description paragraph(s)...

As per coding guidelines, `path/**`: "quote..."    (optional, references project rules)

Also applies to: X-Y, X-Y    (optional, other line ranges with same issue)

<details><summary>Proposed fix</summary>
```lang
code suggestion
```
</details>

<details><summary>Prompt for AI Agents</summary>
prompt text...
</details>
```

Key fields to extract:
- **File path**: from the `<details><summary>` wrapping the file group
- **Line range**: backtick-formatted `` `X-Y` `` at the start of each comment (may also appear in the file summary as `path.ext-X-Y`)
- **Severity**: emoji + type label and optional color severity (see severity_guide.md)
- **Title**: bold text after the severity line
- **"Also applies to"**: additional line ranges in the same file with the same issue
- **Proposed fix / Suggested fix**: code suggestion inside `<details>`. Summary text varies widely, with optional emoji prefix and description. Examples: `Proposed fix`, `Suggested fix`, `🔧 Proposed fix (...)`, `💡 Proposed fix`, `🔒 Suggested direction`, `✨ Optional: ...`, `♻️ Suggested cleanup`, `🔎 Suggested assertion hardening`, `♻️ Suggested diff`. Match any `<details>` block whose summary contains "fix", "suggest", "proposed", or "optional"
- **Prompt for AI Agents**: per-comment context prompt inside `<details>`

## Using the "Prompt for AI Agents"

CodeRabbit provides two levels of AI prompts:

### Per-comment prompt
Inside each comment's `<details><summary>Prompt for AI Agents</summary>` block. Contains:
- The specific file and line range
- The issue description with context
- References to coding guidelines or project conventions
- The suggested fix approach

### Global prompt
At the bottom of the review body, inside `<details><summary>Prompt for all review comments with AI agents</summary>`. Contains:
- Aggregated context for all comments in the review
- File paths, line ranges, and descriptions for every comment
- Useful for batch processing multiple comments at once

**How to use these prompts**:
1. When processing a comment, check if it has a per-comment prompt
2. If present, use it to understand the issue and suggested approach
3. Always read the actual code before proposing a fix, even when the prompt provides context
4. For batch processing, use the global prompt to understand all issues at once before diving into individual fixes

## Inline comments vs review body comments

CodeRabbit posts comments in two ways:

| Type | API endpoint | When used |
|------|-------------|-----------|
| Inline review comments | `pulls/$PR/comments` | Comments on lines within the PR diff |
| Review body sections | `pulls/$PR/reviews` | Outside diff, duplicate, nitpick comments |
| Review-attached inline comments | `pulls/$PR/reviews/$REVIEW_ID/comments` | Fallback for inline comments not yet surfaced by the general endpoint |

**ALWAYS** fetch both endpoints to get the complete picture. Inline comments may reference issues also mentioned in the review body (especially duplicates).

### Review-attached comment gap

CodeRabbit's "actionable comments" are posted as part of a review object. The general `pulls/$PR/comments` endpoint may not surface these comments, or may surface them with a delay. When the review body states "Actionable comments posted: N" but the general endpoint returns fewer than N new originals from CodeRabbit, fetch the missing comments via the review-specific endpoint:

```bash
gh api repos/$REPO/pulls/$PR/reviews/$REVIEW_ID/comments?per_page=100 --jq '
  [.[] | select(.in_reply_to_id == null) |
   {id, path, user: .user.login, created_at, body: .body[0:200]}]
'
```

Deduplicate by `id` against the general endpoint results. Comments found only via this endpoint are standard inline comments and support the same `in_reply_to` reply mechanism.

## "Also applies to" handling

Some comments include `Also applies to: 258-266, 291-296`. These indicate the same issue exists at multiple locations in the same file. When fixing:

1. Fix the primary location (the one with the full description)
2. Apply the same fix pattern to all "also applies to" ranges
3. Verify each location, as the exact code may differ slightly

## Duplicate comments

Comments in the "Duplicate comments" section were already flagged in a previous review. They reappear because the underlying issue was not fixed. Treat them as:

- Same severity as indicated in their label
- Higher actual priority than their label suggests (reviewer is repeating themselves)
- Check if they were previously deferred or missed

## Configuration reference

CodeRabbit behavior is controlled via `.coderabbit.yaml` in the repo root:

```yaml
reviews:
  profile: "chill"                      # chill (default) or assertive (includes nitpicks)
  enable_prompt_for_ai_agents: true     # includes "Prompt for AI Agents" in comments
```

- `chill`: lighter feedback, nitpick sections are hidden
- `assertive`: full feedback, includes nitpick and minor comments

Official docs: https://docs.coderabbit.ai/guides/code-review-overview
