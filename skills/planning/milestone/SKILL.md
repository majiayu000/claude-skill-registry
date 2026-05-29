---
description: When users mention a milestone version (e.g., "0.4.0", "v0.4.0") or ask about release status, invoke this skill to analyze GitHub milestone progress, issues, and suggest next steps.
argument-hint: [version]
allowed-tools: Bash(gh api:*), Bash(gh issue list:*), Bash(gh issue view:*)
context: fork
model: haiku
---

# Milestone Status Summary

Analyze and summarize the status of a GitHub milestone for this repository.

## Arguments

- `$ARGUMENTS`: The milestone version (e.g., "v0.4.0" or "0.4.0"). If not provided, list available milestones.

## Instructions

You are a milestone analysis agent. Your job is to query GitHub and provide a concise summary of milestone status.

### If no milestone specified

List all open milestones with their descriptions:

```bash
gh api repos/zeroae/zae-limiter/milestones --jq '.[] | "- \(.title): \(.description)"'
```

### If milestone specified

1. **Get milestone details:**
   ```bash
   gh api repos/zeroae/zae-limiter/milestones --jq '.[] | select(.title == "vX.Y.Z") | {title, description, state, open_issues, closed_issues}'
   ```

2. **List all issues in the milestone:**
   ```bash
   gh issue list --milestone "vX.Y.Z" --state all --json number,title,state,labels --jq '.[] | "\(.state)\t#\(.number)\t\(.title)"'
   ```

3. **If there's an epic issue (title starts with "🎯"), get its body for context:**
   ```bash
   gh issue view <epic-number> --json title,body
   ```

### Output Format

Provide a summary in this format:

```
## Milestone vX.Y.Z: <Description>

**Theme:** <from epic or milestone description>

**Progress:** X closed / Y open issues

### Open Issues

| # | Title | Notes |
|---|-------|-------|
| ... | ... | ... |

### Closed Issues

| # | Title |
|---|-------|
| ... | ... |

### Analysis

<Brief analysis of what's done, what remains, and any blockers>

### Suggested Next Steps

1. <action>
2. <action>
```

### Important

- Normalize milestone input: if user provides "0.4.0", search for "v0.4.0"
- Keep the summary concise - don't include full issue bodies
- Highlight blockers or dependencies if mentioned in issue titles/bodies
- For epics, check success criteria completion status
