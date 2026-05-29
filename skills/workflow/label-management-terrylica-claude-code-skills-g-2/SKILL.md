---
name: label-management
description: GitHub label and milestone management. TRIGGERS - create label, edit label, manage milestones, issue taxonomy.
---

# Label & Milestone Management

**Capability:** Complete label and milestone CRUD operations with native GitHub CLI

**When to use:** Managing labels, milestones, and metadata organization

**No Extension Required:** All operations use native `gh` commands

---

## Label Operations

### List Labels

```bash
# List all labels
gh label list

# List with JSON output
gh label list --json name,color,description

# Filter and format
gh label list --json name,color --jq '.[] | "\(.name): #\(.color)"'
```

### Create Labels

```bash
# Basic creation
gh label create "bug" --color "ff0000" --description "Something isn't working"

# Multiple labels at once
gh label create "priority:high" --color "ff0000"
gh label create "priority:medium" --color "ffaa00"
gh label create "priority:low" --color "00ff00"

# Knowledge base labels
gh label create "claude-code" --color "0366d6" --description "Claude Code tips and tricks"
gh label create "github-cli" --color "2ea44f" --description "GitHub CLI workflows"
```

### Update Labels

```bash
# Update color
gh label edit "bug" --color "d73a4a"

# Update description
gh label edit "bug" --description "Confirmed bugs"

# Rename label
gh label edit "old-name" --name "new-name"
```

### Delete Labels

```bash
# Delete single label
gh label delete "wontfix"

# Delete with confirmation skip
gh label delete "duplicate" --yes

# Batch delete (careful!)
gh label list --json name --jq '.[].name' | grep "temp-" | xargs -I {} gh label delete {} --yes
```

---

## Label Organization Strategies

### Knowledge Base Labels

```bash
# Topic categories
gh label create "claude-code" --color "0366d6"
gh label create "github-cli" --color "2ea44f"
gh label create "git" --color "5319e7"
gh label create "terminal" --color "0e8a16"

# Content types
gh label create "tips" --color "c5def5"
gh label create "troubleshooting" --color "d93f0b"
gh label create "how-to" --color "bfdadc"
gh label create "reference" --color "d4c5f9"
gh label create "example" --color "c2e0c6"

# Workflows
gh label create "workflow" --color "fbca04"
gh label create "mcp" --color "f9d0c4"
```

### Priority System

```bash
# Hierarchical priorities
gh label create "priority:critical" --color "b60205" --description "Urgent - immediate action required"
gh label create "priority:high" --color "d93f0b" --description "Important - address soon"
gh label create "priority:medium" --color "fbca04" --description "Normal priority"
gh label create "priority:low" --color "0e8a16" --description "Low priority - nice to have"
```

### Status Tracking

```bash
# Workflow states
gh label create "status:needs-triage" --color "ededed"
gh label create "status:in-progress" --color "fbca04"
gh label create "status:blocked" --color "d93f0b"
gh label create "status:review" --color "0366d6"
gh label create "status:ready" --color "0e8a16"
```

---

## Cloning Labels Between Repositories

```bash
# Export labels from source repo
gh label list --repo source-owner/source-repo --json name,color,description > labels.json

# Import to target repo
cat labels.json | jq -r '.[] | @sh "gh label create \(.name) --color \(.color) --description \(.description) --repo target-owner/target-repo"' | sh
```

---

## Milestone Operations

### List Milestones

```bash
# Using gh api (no native gh milestone command)
gh api repos/{owner}/{repo}/milestones --jq '.[] | {number, title, state}'

# With full details
gh api repos/{owner}/{repo}/milestones --jq '.[] | {number, title, description, due_on, state, open_issues, closed_issues}'
```

### Create Milestone

```bash
# Basic milestone
gh api repos/{owner}/{repo}/milestones \
  --method POST \
  --field title="v1.0.0" \
  --field description="First stable release" \
  --field due_on="2025-12-31T23:59:59Z"

# With state (open/closed)
gh api repos/{owner}/{repo}/milestones \
  --method POST \
  --field title="Q1 2025" \
  --field state="open"
```

### Update Milestone

```bash
# Update milestone
gh api repos/{owner}/{repo}/milestones/MILESTONE_NUMBER \
  --method PATCH \
  --field title="Updated Title" \
  --field description="Updated description" \
  --field state="closed"
```

### Delete Milestone

```bash
# Delete milestone
gh api repos/{owner}/{repo}/milestones/MILESTONE_NUMBER --method DELETE
```

---

## Batch Label Operations

### Apply Label to Multiple Issues

```bash
# Add label to all open bugs
gh issue list --label bug --state open --json number --jq '.[].number' | \
  xargs -I {} gh issue edit {} --add-label priority:high

# Remove label from closed issues
gh issue list --label needs-triage --state closed --json number --jq '.[].number' | \
  xargs -I {} gh issue edit {} --remove-label needs-triage
```

### Rename Labels Across Issues

```bash
# 1. Get all issues with old label
ISSUES=$(gh issue list --label old-label --json number --jq '.[].number')

# 2. Add new label, remove old label
for issue in $ISSUES; do
  gh issue edit $issue --add-label new-label --remove-label old-label
done

# 3. Delete old label
gh label delete old-label
```

---

## Label Analytics

### Label Usage Statistics

```bash
#!/bin/bash
# Count issues per label

gh label list --json name --jq '.[].name' | while read -r label; do
  count=$(gh issue list --label "$label" --json number --jq '. | length')
  echo "$label: $count issues"
done | sort -t: -k2 -rn
```

### Milestone Progress

```bash
# Get milestone progress
gh api repos/{owner}/{repo}/milestones/MILESTONE_NUMBER --jq '{
  title,
  open: .open_issues,
  closed: .closed_issues,
  percent_complete: ((.closed_issues / (.open_issues + .closed_issues)) * 100 | round)
}'
```

---

## Common Workflows

### Knowledge Base Setup

```bash
# 1. Create label structure
gh label create "claude-code" --color "0366d6"
gh label create "tips" --color "c5def5"
gh label create "how-to" --color "bfdadc"

# 2. Create issues with labels
gh issue create --title "Tip: Plan Mode" --label claude-code,tips,how-to --body-file tip.md

# 3. Search by label
gh search issues --label claude-code,tips
```

### Issue Triage Workflow

```bash
# 1. List untriaged issues
gh issue list --label needs-triage

# 2. Review and categorize
gh issue edit 123 --add-label bug,priority:high --remove-label needs-triage

# 3. Assign milestone
gh api repos/{owner}/{repo}/issues/123 --method PATCH --field milestone=1
```

---

## Color Palette (Standard GitHub)

| Color  | Hex       | Use Case                |
| ------ | --------- | ----------------------- |
| Red    | `#d73a4a` | Bugs, critical          |
| Orange | `#d93f0b` | Warnings, high priority |
| Yellow | `#fbca04` | Medium priority, needs  |
| Green  | `#0e8a16` | Improvements, low       |
| Blue   | `#0366d6` | Enhancements, features  |
| Purple | `#5319e7` | Questions, research     |
| Gray   | `#ededed` | Meta, wontfix           |

---

## Best Practices

1. **Consistent naming** - Use prefixes for hierarchies (`priority:high`, `type:bug`)
2. **Clear descriptions** - Help users understand when to use each label
3. **Limited set** - 10-20 core labels, avoid label proliferation
4. **Color coding** - Use colors meaningfully (red=urgent, green=low-priority)
5. **Regular cleanup** - Remove unused labels, consolidate duplicates
6. **Document system** - Maintain label guide in repository docs

---

## Label Anti-Patterns

❌ **Too many labels** - Hard to choose, inconsistent application
❌ **Duplicate meanings** - "bug" vs "defect" vs "broken"
❌ **Unclear names** - "label1", "misc", "other"
❌ **No descriptions** - Users don't know when to apply
❌ **Random colors** - No meaningful color coding

---

## Migration: Deprecated Extensions

**DON'T USE:**

- `gh-label` extension (last updated 2022) → Use native `gh label` instead
- `gh-milestone` extension (last updated 2023) → Use `gh api` instead

**Native commands are:**

- ✅ Better maintained
- ✅ Faster (no extension overhead)
- ✅ More reliable
- ✅ Always available

---

**Empirical Testing:** 40+ test cases covering all label operations

**Full Operational Guide:** [AI_AGENT_OPERATIONAL_GUIDE.md](/docs/guides/AI_AGENT_OPERATIONAL_GUIDE.md)
