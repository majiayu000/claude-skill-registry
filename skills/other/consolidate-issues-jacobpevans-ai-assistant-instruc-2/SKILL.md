---
title: consolidate-issues
description: >
  Reduce GitHub issue backlog through deduplication, linking, and closure. Use
  before creating new issues, when enforcement_mode is CONSOLIDATION, when
  issue:PR ratio exceeds 3:1, when AI-created issues reach 25, or when total
  issues approach 50.
---

<!-- markdownlint-disable-file MD013 -->

Reduces issue backlog to prevent AI-created issue spam and maintain healthy project hygiene.

## When to Use This Skill

- Before creating any new GitHub issue (always check limits first)
- When preflight returns `enforcement_mode: CONSOLIDATION`
- When issue:PR ratio exceeds 3:1
- When AI-created issues reach 25
- When total open issues approach 50
- Proactively during maintenance cycles

## Enforcement Modes

| Mode | Trigger | Action |
| ------ | --------- | -------- |
| NORMAL | All limits OK | Work normally |
| CONSOLIDATION | AI-created >= 25 or ratio > 3 | Run this skill first |
| PR_CREATION | Ratio > 5, PRs < 3 | Create PRs, not issues |
| PR_FOCUS | Open PRs >= 10 | Resolve PRs only |
| PAUSED | Total issues >= 50 | Run skipped entirely |

## Hard Limits

- **50 total issues**: Run paused
- **25 AI-created issues**: Skip issue creation
- **10 open PRs**: PR_FOCUS mode
- **3:1 ratio**: CONSOLIDATION mode

## Consolidation Workflow

### Step 1: Check Current Counts

```bash
TOTAL=$(gh issue list --state open --json number | jq length)
AI=$(gh issue list --state open --label ai-created --json number | jq length)
PRS=$(gh pr list --state open --json number | jq length)
RATIO=$(echo "scale=1; $TOTAL / ($PRS + 1)" | bc)
echo "Total: $TOTAL, AI: $AI, PRs: $PRS, Ratio: $RATIO:1"
```

### Step 2: Fetch All Open Issues

```bash
gh issue list --state open --limit 100 --json number,title,body,labels,createdAt
```

### Step 3: Close Duplicates

Identify duplicate issues. For each duplicate issue number, run the following commands as separate tool calls:

**For issue #123:**

```bash
gh issue edit 123 --add-label duplicate
gh issue close 123 --reason "not planned" \
  --comment "Duplicate of #456. Closing."
```

**For issue #124:**

```bash
gh issue edit 124 --add-label duplicate
gh issue close 124 --reason "not planned" \
  --comment "Duplicate of #456. Closing."
```

### Step 4: Close Resolved Issues

Search for issues fixed by merged PRs:

```bash
gh pr list --state merged --limit 50 --json number,title,body
```

For each issue resolved by a merged PR, run the following command as a separate tool call:

```bash
gh issue close 456 --reason completed \
  --comment "Resolved by PR #789."
```

### Step 5: Link Related Issues

For related (non-duplicate) issues, run the following command as a separate tool call for each related issue pair:

```bash
gh issue comment 123 --body "Related to #456."
```

For 3+ related issues, create an umbrella issue as a separate tool call.

### Step 6: Report Summary

Document consolidation results:

- Duplicates closed: N
- Issues resolved by merged PRs: K
- Related issues linked: M

## Best Practices

1. **Check before creating** - Always verify limits first
2. **Close aggressively** - When in doubt, close as duplicate/resolved
3. **Report to Slack** - Never create issues for status updates
4. **Focus on PRs** - PRs close issues; issues don't close themselves
