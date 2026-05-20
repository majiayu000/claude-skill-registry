---
name: standup
description: Use when preparing daily standup notes or summarizing recent PR and commit activity for team updates.
effort: medium
argument-hint: "--days N|--author <name>"
---



# Standup

## Purpose

Generate standup notes from actual PR and commit activity. Produces concise, copy-paste-ready summaries grouped by status. Eliminates manual standup preparation.

## Trigger

- Command: `/ai-standup`
- Context: preparing for daily standup, team sync, or async status update.

## When to Use

- Before daily standup meetings
- Async status updates for Slack/Teams channels
- End-of-day summaries
- Handoff notes between sessions

## When NOT to Use

- **Sprint-level summaries** -- use `/ai-sprint retro`
- **Incident timelines** -- use `/ai-postmortem`

## Pre-conditions (MANDATORY)

1. Read `.ai-engineering/manifest.yml` — `work_items` section.
2. Use the active provider to gather work item data:
   - **GitHub**: `gh issue list --label <team_label> --state all --json ...`
   - **Azure DevOps**: `az boards query --wiql "..."` filtered by `area_path` and current iteration
3. Include work item status in standup notes when available.

## Procedure

1. **Determine lookback** -- default: 1 working day. Override with `--days N`. Skip weekends unless `--days` explicitly covers them.

2. **Collect activity** -- scan the following sources:
   a. `git log --since="N days ago" --author="<name>"` -- local commits
   b. `gh pr list --author="<name>" --state=all --json title,url,state,updatedAt` -- PRs
   c. Active spec tasks from `.ai-engineering/specs/spec.md` and `specs/plan.md` -- current work

3. **Classify items** into three groups:

   | Group | Criteria |
   |-------|----------|
   | **Shipped** | Merged PRs, completed spec tasks |
   | **In Progress** | Open PRs, branches with recent commits, active spec tasks |
   | **Blocked** | PRs with review requests pending 24h+, tasks marked blocked |

4. **Format output** -- markdown to stdout:

```markdown
## Standup — YYYY-MM-DD

### Shipped
- Merged PR #123: Add secret scanning to commit hook [link]
- spec-054: Task 2.1 -- hook installation complete

### In Progress
- PR #125: Telemetry event schema (awaiting review) [link]
- spec-054: Task 3.2 -- guard event integration

### Blocked
- PR #120: Dependency update blocked on upstream release
```

5. **Author resolution** -- if `--author` not specified, detect from `git config user.name` or `gh api user`.

## Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--days N` | 1 | Lookback period in working days |
| `--author <name>` | current user | Filter by author name or GitHub handle |

## Quick Reference

```
/ai-standup                   # today's standup
/ai-standup --days 3          # last 3 days (covers a long weekend)
/ai-standup --author @alice   # standup for a specific team member
```

## Output

- Markdown to stdout (not saved to file)
- Designed for copy-paste into Slack, Teams, or standup tools
- Each item includes a link when available

$ARGUMENTS
