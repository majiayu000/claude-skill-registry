---
name: update-plan-from-subissues
description: Update PLANS.md content based on linked sub-issues status
disable-model-invocation: true
---

# Update Plan from Sub-issues

Update PLANS.md by analyzing linked sub-issues and reflecting their current state.

## Arguments

$ARGUMENTS

## Process

### 1. Read PLANS.md frontmatter

Extract `issue:` field (parent issue number). If not found, exit with error.

### 2. Fetch sub-issues from parent

```bash
gh api repos/{owner}/{repo}/issues/{issue}/sub_issues \
  --jq '.[] | {number, title, state}'
```

### 3. Analyze sub-issues and PLANS.md content

For each sub-issue:
```bash
gh issue view {sub-issue-number} --json number,title,body,state
```

Identify what needs updating:
- **Validation & Acceptance Criteria**: Mark completed items
- **Open Questions**: Remove resolved questions
- **Discoveries & Insights**: Add findings from discussions
- **Decision Log**: Add decisions made in sub-issues
- **Follow-up Issues**: Update with new sub-issues

### 4. Update PLANS.md

- Use Edit tool to update existing content
- Mark checkboxes `- [x]` for completed sub-issues
- Keep existing structure unchanged

### 5. Sync to GitHub (optional)

After updating, offer to run `/sync-plan`.

## Guidelines

- Do NOT add new sections
- Do NOT duplicate current information
- Only update content reflecting sub-issue progress
- Preserve existing narrative and structure
