---
name: pr-merge-watcher
description: Checks for merged PRs and updates Notion to Done. Use daily or on-demand to close out completed tickets after PR merge.
---

# PR Merge Watcher

Scans open pipeline runs for merged PRs and updates Notion status to Done. Handles the common case where the agent is closed before PR merge.

## When to Use

- Daily maintenance check
- After you know PRs have merged
- Resume pipeline-tracker shows stale "In Review" tickets

## Workflow

### 1. Find Open Runs

Scan for runs in "pr-created" or "in-review" status:

```bash
find runs/ -name "status.json" -exec jq -c \
  'select(.status | test("pr-created|in-review|ci-passed")) |
   {id: .ticketId, status: .status, prNumber: .prNumber, prUrl: .prUrl}' {} \; \
  2>/dev/null | grep -v '^$'
```

### 2. Check PR Merge Status

For each open run with a PR:

```bash
PR_NUMBER=123
gh pr view $PR_NUMBER --json state,mergedAt --jq '{state, mergedAt}'
```

Possible states:

- `OPEN` - PR still open, skip
- `MERGED` - PR merged, update Notion
- `CLOSED` - PR closed without merge, mark as abandoned

### 3. Update Notion for Merged PRs

**⚠️ Follow [Notion Write Safety](docs/notion-write-safety.md) rules.**

For each merged PR:

```bash
# Get ticket page ID from status.json
PAGE_ID=$(jq -r '.notionPageId' "runs/$TICKET_ID/status.json")

# Update via Notion MCP
# Status: In Review → Done
```

Log the write:

```json
{
  "notionWrites": [
    {
      "field": "Status",
      "value": "Done",
      "previousValue": "In Review",
      "at": "...",
      "skill": "pr-merge-watcher",
      "success": true
    }
  ]
}
```

### 4. Update Local Status

```bash
jq '.status = "done" | .completedAt = now | .mergedAt = .prMergedAt' \
  "runs/$TICKET_ID/status.json" > tmp && mv tmp "runs/$TICKET_ID/status.json"
```

### 5. Handle Closed (Not Merged)

If PR was closed without merging:

```markdown
⚠️ PR #123 was closed without merging

Ticket: {ticket title}
PR: {pr url}

Options:

1. Mark ticket as abandoned (Status → Not Started)
2. Keep current status (investigate later)
3. Archive run locally only

Your choice:
```

### 6. Generate Report

```markdown
# PR Merge Watcher Report

**Scanned:** {timestamp}
**Runs checked:** {N}

## Merged PRs (Updated to Done)

| Ticket  | PR   | Merged At  |
| ------- | ---- | ---------- |
| ABC-123 | #456 | 2024-01-15 |
| DEF-456 | #789 | 2024-01-16 |

## Still Open

| Ticket  | PR   | Status          | Age    |
| ------- | ---- | --------------- | ------ |
| GHI-789 | #101 | Awaiting review | 3 days |

## Closed Without Merge

| Ticket  | PR   | Action Taken     |
| ------- | ---- | ---------------- |
| JKL-012 | #102 | Marked abandoned |

## Summary

- **Completed:** 2 tickets marked Done
- **Open:** 1 PR awaiting review
- **Abandoned:** 1 closed PR
```

## Batch Mode

Run without prompts for automation:

```bash
# Auto-update all merged PRs, skip closed ones
amp -c "/skill pr-merge-watcher --batch"
```

In batch mode:

- Merged PRs → Auto-update to Done
- Closed PRs → Log warning, don't modify
- Open PRs → Skip silently

## Scheduled Execution

Add to daily workflow:

```bash
# Morning check
0 9 * * * cd ~/repos/ticket-to-pr-pipeline && amp -c "/skill pr-merge-watcher --batch" >> logs/merge-watcher.log 2>&1
```

Or integrate with pipeline-tracker:

```markdown
When running `/skill pipeline-tracker`:

1. Show dashboard
2. Auto-run pr-merge-watcher check
3. Report any newly completed tickets
```

## GitHub Webhook Alternative

For real-time updates, set up a GitHub webhook:

1. Create webhook on repo for `pull_request` events
2. Filter for `action: closed` with `merged: true`
3. Trigger Notion update via API

This is more complex but provides instant updates.

## Edge Cases

### PR Merged to Different Branch

If PR merged to non-main branch (e.g., staging):

- Check if eventually merged to main
- Or mark as "partial" completion

### Multiple PRs per Ticket (Stacked)

Check stack.json for multi-PR tickets:

- All PRs merged → Done
- Some merged → Keep In Review
- Track individual PR states

### Notion Page Deleted

If ticket page no longer exists:

- Log error
- Archive run locally
- Don't retry

## Integration with Pipeline

**Trigger Points:**

- Manual: `/skill pr-merge-watcher`
- Via pipeline-tracker dashboard
- Scheduled cron job
- GitHub webhook (advanced)

**Status Transitions:**

- `in-review` + PR merged → `done`
- `in-review` + PR closed → `abandoned`

## Output Artifacts

| File                 | Location                       | Description                 |
| -------------------- | ------------------------------ | --------------------------- |
| status.json          | `runs/{ticket-id}/status.json` | Updated with done/abandoned |
| merge-watcher-log.md | `runs/merge-watcher-log.md`    | Historical report           |
