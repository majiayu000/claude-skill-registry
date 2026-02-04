---
name: milestone-management
description: Use for time-based grouping of issues into delivery phases. Creates, updates, and tracks milestones, associates issues and epics, monitors progress toward milestone completion.
---

# Milestone Management

## Overview

**Milestones** group issues by delivery phase or time period. They answer "what will be done by when?"

**Core principle:** Milestones are delivery commitments. Track them closely.

**Announce at start:** "I'm using milestone-management to organize work into delivery phases."

## What is a Milestone?

A milestone is:
- A GitHub milestone with a title, description, and optional due date
- A collection of issues and epics targeting that delivery phase
- A progress tracker showing completion percentage

## Milestone vs Epic

| Aspect | Milestone | Epic |
|--------|-----------|------|
| **Grouping by** | Time/delivery phase | Feature/capability |
| **Scope** | Cross-cutting | Focused |
| **Can contain** | Multiple epics | Related issues |
| **Progress** | % of issues closed | % of issues closed |
| **Due date** | Usually has one | Usually doesn't |

An epic can be assigned to a milestone. Multiple epics can share a milestone.

## Creating a Milestone

### Via GitHub CLI

```bash
# Create milestone with due date
gh api repos/$GITHUB_OWNER/$GITHUB_REPO/milestones \
  -X POST \
  -f title="[NAME]" \
  -f description="[DESCRIPTION]" \
  -f due_on="YYYY-MM-DDTHH:MM:SSZ"

# Create milestone without due date
gh api repos/$GITHUB_OWNER/$GITHUB_REPO/milestones \
  -X POST \
  -f title="[NAME]" \
  -f description="[DESCRIPTION]"
```

### Milestone Naming Conventions

| Pattern | Example | Use Case |
|---------|---------|----------|
| Version | `v1.0.0` | Release milestones |
| Quarter | `Q1 2026` | Quarterly planning |
| Phase | `Phase 1: Foundation` | Initiative phases |
| Sprint | `Sprint 23` | Agile sprints |
| Date | `2026-01 January` | Monthly releases |

### Milestone Description Template

```markdown
## [MILESTONE NAME]

### Goals
- [Primary goal 1]
- [Primary goal 2]

### Epics Included
- #[EPIC_1] - [Epic Title]
- #[EPIC_2] - [Epic Title]

### Key Deliverables
1. [Deliverable 1]
2. [Deliverable 2]
3. [Deliverable 3]

### Success Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]

### Dependencies
- Requires: [Previous milestone or external dependency]
- Enables: [What this milestone unblocks]

---
**Target Date:** [DATE]
**Owner:** [Team/Person]
```

## Assigning Issues to Milestones

### Assign During Creation

```bash
gh issue create \
  --title "[Title]" \
  --milestone "[MILESTONE_NAME]" \
  --body "[Body]"
```

### Assign Existing Issue

```bash
gh issue edit [ISSUE_NUMBER] --milestone "[MILESTONE_NAME]"
```

### Assign Epic to Milestone

```bash
# Assign the epic tracking issue
gh issue edit [EPIC_NUMBER] --milestone "[MILESTONE_NAME]"

# Assign all issues in the epic
gh issue list --label "epic-[NAME]" --json number --jq '.[].number' | \
  while read num; do
    gh issue edit "$num" --milestone "[MILESTONE_NAME]"
  done
```

## Tracking Milestone Progress

### View Milestone Status

```bash
# List milestones with progress
gh api repos/$GITHUB_OWNER/$GITHUB_REPO/milestones \
  --jq '.[] | "\(.title): \(.open_issues) open, \(.closed_issues) closed"'

# Get specific milestone details
gh api repos/$GITHUB_OWNER/$GITHUB_REPO/milestones/[NUMBER] \
  --jq '{title, open_issues, closed_issues, due_on, description}'
```

### List Issues in Milestone

```bash
# All issues in milestone
gh issue list --milestone "[MILESTONE_NAME]"

# Open issues in milestone
gh issue list --milestone "[MILESTONE_NAME]" --state open

# Closed issues in milestone
gh issue list --milestone "[MILESTONE_NAME]" --state closed
```

### Progress Report

Generate a progress report:

```bash
# Get milestone data
MILESTONE_DATA=$(gh api repos/$GITHUB_OWNER/$GITHUB_REPO/milestones/[NUMBER])

TITLE=$(echo "$MILESTONE_DATA" | jq -r '.title')
OPEN=$(echo "$MILESTONE_DATA" | jq -r '.open_issues')
CLOSED=$(echo "$MILESTONE_DATA" | jq -r '.closed_issues')
TOTAL=$((OPEN + CLOSED))
PERCENT=$((CLOSED * 100 / TOTAL))
DUE=$(echo "$MILESTONE_DATA" | jq -r '.due_on')

echo "## Milestone: $TITLE"
echo "**Progress:** $CLOSED / $TOTAL ($PERCENT%)"
echo "**Open:** $OPEN issues"
echo "**Due:** $DUE"
```

## Milestone Lifecycle

```
┌────────────┐     ┌────────────┐     ┌────────────┐     ┌────────────┐
│  Planning  │────▶│   Active   │────▶│  Closing   │────▶│   Closed   │
└────────────┘     └────────────┘     └────────────┘     └────────────┘
     │                   │                   │                  │
     ▼                   ▼                   ▼                  ▼
  Adding              Work in            Finishing         All issues
  issues              progress           last items        resolved
```

### Milestone States

| State | Indicators |
|-------|------------|
| Planning | Issues being added, 0% complete |
| Active | Work in progress, 1-80% complete |
| Closing | Final stretch, 80-99% complete |
| Closed | 100% complete, milestone closed |

## Updating Milestones

### Update Description/Due Date

```bash
# Update due date
gh api repos/$GITHUB_OWNER/$GITHUB_REPO/milestones/[NUMBER] \
  -X PATCH \
  -f due_on="YYYY-MM-DDTHH:MM:SSZ"

# Update description
gh api repos/$GITHUB_OWNER/$GITHUB_REPO/milestones/[NUMBER] \
  -X PATCH \
  -f description="[NEW_DESCRIPTION]"
```

### Close a Milestone

```bash
gh api repos/$GITHUB_OWNER/$GITHUB_REPO/milestones/[NUMBER] \
  -X PATCH \
  -f state="closed"
```

## Milestone Planning Patterns

### Initiative Phases

For large initiatives, create phase milestones:

```bash
# Phase 1: Foundation
gh api repos/$GITHUB_OWNER/$GITHUB_REPO/milestones -X POST \
  -f title="[Initiative] Phase 1: Foundation" \
  -f description="Infrastructure and setup for [Initiative Name]"

# Phase 2: Core Features
gh api repos/$GITHUB_OWNER/$GITHUB_REPO/milestones -X POST \
  -f title="[Initiative] Phase 2: Core Features" \
  -f description="Primary feature implementation"

# Phase 3: Polish & Launch
gh api repos/$GITHUB_OWNER/$GITHUB_REPO/milestones -X POST \
  -f title="[Initiative] Phase 3: Polish & Launch" \
  -f description="Final testing, polish, and release"
```

### Release Milestones

For version-based releases:

```bash
gh api repos/$GITHUB_OWNER/$GITHUB_REPO/milestones -X POST \
  -f title="v2.0.0" \
  -f description="Major release with [features]" \
  -f due_on="2026-03-01T00:00:00Z"
```

### Quarterly Milestones

For quarterly planning:

```bash
gh api repos/$GITHUB_OWNER/$GITHUB_REPO/milestones -X POST \
  -f title="Q1 2026" \
  -f description="Q1 2026 deliverables" \
  -f due_on="2026-03-31T23:59:59Z"
```

## Handling Slippage

When issues won't make a milestone:

### Option 1: Move to Next Milestone

```bash
gh issue edit [ISSUE_NUMBER] --milestone "[NEXT_MILESTONE]"
```

### Option 2: Extend Milestone

```bash
gh api repos/$GITHUB_OWNER/$GITHUB_REPO/milestones/[NUMBER] \
  -X PATCH \
  -f due_on="[NEW_DATE]"
```

### Option 3: Reduce Scope

Move non-critical issues out:

```bash
# Remove from milestone (set to no milestone)
gh issue edit [ISSUE_NUMBER] --milestone ""
```

### Document Slippage

```bash
gh issue comment [EPIC_OR_INITIATIVE] --body "## Milestone Update

**Milestone:** [NAME]
**Original Due:** [DATE]
**Status:** At risk

**Issues slipping:**
- #[N] - [Reason]
- #[N] - [Reason]

**Action taken:**
- [Moved X issues to next milestone]
- [Extended deadline by Y days]
- [Descoped Z items]"
```

## Milestone Reports

### Weekly Status Report

```markdown
## Milestone Status Report - [DATE]

### [MILESTONE 1]
- **Progress:** 12/20 (60%)
- **Due:** [DATE]
- **Status:** 🟢 On Track
- **Blockers:** None

### [MILESTONE 2]
- **Progress:** 3/15 (20%)
- **Due:** [DATE]
- **Status:** 🟡 At Risk
- **Blockers:** Waiting on #123

### [MILESTONE 3]
- **Progress:** 0/10 (0%)
- **Due:** [DATE]
- **Status:** ⚪ Not Started
- **Blockers:** Depends on Milestone 2
```

### Generate Report Script

```bash
echo "# Milestone Status Report - $(date +%Y-%m-%d)"
echo ""

gh api repos/$GITHUB_OWNER/$GITHUB_REPO/milestones --jq '.[] |
  "## \(.title)\n- **Progress:** \(.closed_issues)/\(.open_issues + .closed_issues)\n- **Due:** \(.due_on // "No due date")\n"'
```

## Memory Integration

```bash
mcp__memory__create_entities([{
  "name": "Milestone-[NAME]",
  "entityType": "Milestone",
  "observations": [
    "Created: [DATE]",
    "Due: [DATE]",
    "Repository: $GITHUB_REPO",
    "Epics: [LIST]",
    "Issues: [COUNT]",
    "Status: [Planning/Active/Closed]"
  ]
}])
```

## Checklist

- [ ] Created milestone with clear name
- [ ] Added description with goals
- [ ] Set due date (if applicable)
- [ ] Assigned epics to milestone
- [ ] Assigned issues to milestone
- [ ] Documented in initiative (if applicable)
- [ ] Set up progress tracking
- [ ] Stored in knowledge graph
