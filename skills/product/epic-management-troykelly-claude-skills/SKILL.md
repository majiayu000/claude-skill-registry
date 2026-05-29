---
name: epic-management
description: Use for LARGE work requiring feature-level grouping. Creates epic tracking issues, manages related issues under a common label, tracks epic progress, and coordinates with milestones.
allowed-tools:
  - Bash
  - mcp__github__*
model: opus
---

# Epic Management

## Overview

An **epic** groups related issues that together deliver a feature or capability. This skill creates, tracks, and manages epics using GitHub's native features.

**Core principle:** An epic is a collection of issues that together deliver user value.

**Announce at start:** "I'm using epic-management to structure this feature into a tracked epic with related issues."

## What is an Epic?

An epic is:
- A parent issue with the `epic` label
- A collection of related issues sharing an `epic-[name]` label
- Optionally associated with a milestone
- Part of an initiative (if the work is massive)

## Epic Structure in GitHub

```
Epic (Parent Issue)
├── Label: epic
├── Label: epic-[name]
├── Milestone: [optional]
└── Project: [with epic fields]

Related Issues
├── Label: epic-[name]
├── Reference: "Part of #[EPIC_NUMBER]"
└── Milestone: [same as epic]
```

## Creating an Epic

### Step 1: Create Epic Label

```bash
# Create the epic-specific label
gh label create "epic-[SHORT-NAME]" \
  --color "0E8A16" \
  --description "[Brief description of epic goal]"
```

### Step 2: Create Epic Tracking Issue

```bash
gh issue create \
  --title "[Epic] [NAME]" \
  --label "epic,epic-[SHORT-NAME]" \
  --body "## Epic: [NAME]

## Goal
[What this epic delivers when complete]

## Success Criteria
- [ ] [High-level criterion 1]
- [ ] [High-level criterion 2]
- [ ] [High-level criterion 3]

## Context
[Background, why this epic exists, any relevant links]

## Dependencies
- **Requires:** [Other epics/issues that must complete first]
- **Enables:** [Other epics/issues that depend on this]

## Issues

### Ready
- [ ] #[N] - [Title]

### In Progress
[None yet]

### Done
[None yet]

## Progress
**Issues:** 0 / [TOTAL] complete
**Last Updated:** [DATE]

---
## Initiative
[Part of #[INITIATIVE] if applicable, or 'Standalone epic']

## Milestone
[Associated milestone or 'Not assigned']"
```

### Step 3: Add to Project Board (MANDATORY GATE)

**This step is NOT optional. Epics MUST be in the project board.**

```bash
# Get the epic issue URL
EPIC_URL=$(gh issue view [EPIC_NUMBER] --json url -q '.url')

# Add epic to project - REQUIRED
gh project item-add "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" --url "$EPIC_URL"

if [ $? -ne 0 ]; then
  echo "ERROR: Failed to add epic to project. Cannot proceed."
  exit 1
fi

# Get the item ID - REQUIRED
ITEM_ID=$(gh project item-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" \
  --format json | jq -r ".items[] | select(.content.number == [EPIC_NUMBER]) | .id")

if [ -z "$ITEM_ID" ] || [ "$ITEM_ID" = "null" ]; then
  echo "ERROR: Epic added but item ID not found."
  exit 1
fi

echo "Epic #[EPIC_NUMBER] added to project with item ID: $ITEM_ID"
```

### Step 3.5: Set Project Board Fields (MANDATORY)

**All epics must have Type = Epic set in project board.**

```bash
# Get project and field IDs
PROJECT_ID=$(gh project list --owner "$GH_PROJECT_OWNER" --format json | \
  jq -r ".projects[] | select(.number == $GITHUB_PROJECT_NUM) | .id")

STATUS_FIELD_ID=$(gh project field-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" \
  --format json | jq -r '.fields[] | select(.name == "Status") | .id')

TYPE_FIELD_ID=$(gh project field-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" \
  --format json | jq -r '.fields[] | select(.name == "Type") | .id')

# Get option IDs
BACKLOG_OPTION_ID=$(gh project field-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" \
  --format json | jq -r '.fields[] | select(.name == "Status") | .options[] | select(.name == "Backlog") | .id')

EPIC_TYPE_OPTION_ID=$(gh project field-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" \
  --format json | jq -r '.fields[] | select(.name == "Type") | .options[] | select(.name == "Epic") | .id')

# Set Status = Backlog (or Ready if no issues yet to create)
gh project item-edit --project-id "$PROJECT_ID" --id "$ITEM_ID" \
  --field-id "$STATUS_FIELD_ID" --single-select-option-id "$BACKLOG_OPTION_ID"

# Set Type = Epic
gh project item-edit --project-id "$PROJECT_ID" --id "$ITEM_ID" \
  --field-id "$TYPE_FIELD_ID" --single-select-option-id "$EPIC_TYPE_OPTION_ID"

# Verify fields were set
echo "Verifying project board fields..."
VERIFY=$(gh project item-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" \
  --format json | jq ".items[] | select(.content.number == [EPIC_NUMBER])")

echo "Status: $(echo "$VERIFY" | jq -r '.status.name')"
echo "Type: $(echo "$VERIFY" | jq -r '.type.name // "not set"')"
```

**Skill:** `project-board-enforcement`

## Creating Issues Within an Epic

### Issue Template for Epic Issues

```bash
gh issue create \
  --title "[TYPE] [Title]" \
  --label "epic-[SHORT-NAME]" \
  --body "## Description
[What this issue delivers]

Part of epic #[EPIC_NUMBER]: [Epic Title]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Technical Notes
[Any implementation details]

## Dependencies
- Requires: #[N] (if any)
- Blocks: #[N] (if any)"
```

### Linking Issues to Epic

Every issue in an epic must:
1. Have the `epic-[name]` label
2. Reference the epic in description: "Part of epic #[N]"
3. Share the same milestone (if set)
4. **Be in the project board with Status and Type set**
5. **Have Epic field set to parent epic number (if field exists)**

### Adding Child Issues to Project Board (MANDATORY)

```bash
# After creating child issue, add to project board
CHILD_URL=$(gh issue view [CHILD_NUMBER] --json url -q '.url')

gh project item-add "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" --url "$CHILD_URL"

# Get item ID
CHILD_ITEM_ID=$(gh project item-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" \
  --format json | jq -r ".items[] | select(.content.number == [CHILD_NUMBER]) | .id")

# Set Status = Ready
gh project item-edit --project-id "$PROJECT_ID" --id "$CHILD_ITEM_ID" \
  --field-id "$STATUS_FIELD_ID" --single-select-option-id "$READY_OPTION_ID"

# Set Type (Feature, Bug, etc. as appropriate)
gh project item-edit --project-id "$PROJECT_ID" --id "$CHILD_ITEM_ID" \
  --field-id "$TYPE_FIELD_ID" --single-select-option-id "$TYPE_OPTION_ID"

# Link to parent epic (if Epic field exists)
EPIC_FIELD_ID=$(gh project field-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" \
  --format json | jq -r '.fields[] | select(.name == "Epic") | .id')

if [ -n "$EPIC_FIELD_ID" ] && [ "$EPIC_FIELD_ID" != "null" ]; then
  gh project item-edit --project-id "$PROJECT_ID" --id "$CHILD_ITEM_ID" \
    --field-id "$EPIC_FIELD_ID" --text "#[EPIC_NUMBER]"
fi
```

**Skill:** `project-board-enforcement`

## Tracking Epic Progress

### Update Epic Issue Regularly

When issues change status, update the epic:

```bash
gh issue comment [EPIC_NUMBER] --body "## Progress Update - [DATE]

**Completed:** #[N] - [Title]

**Current Status:**
- Ready: [X] issues
- In Progress: [Y] issues
- Done: [Z] issues
- Total: [X+Y+Z] / [TOTAL]

**Next up:** #[N] - [Title]"
```

### Reorganize Epic Body

Keep the epic body current:

```markdown
## Issues

### Ready
- [ ] #102 - Database schema
- [ ] #103 - API endpoints

### In Progress
- [ ] #101 - Initial setup (assignee: @dev)

### Done
- [x] #100 - Research spike

## Progress
**Issues:** 1 / 4 complete (25%)
**Last Updated:** 2025-12-02
```

## Epic Lifecycle

```
┌────────────┐     ┌────────────┐     ┌────────────┐     ┌────────────┐
│  Planning  │────▶│   Active   │────▶│  Closing   │────▶│   Done     │
└────────────┘     └────────────┘     └────────────┘     └────────────┘
     │                   │                   │                  │
     ▼                   ▼                   ▼                  ▼
  Creating            Issues              Last issues       All issues
  issues              in progress         completing        closed
```

### Epic States

| State | Project Status | Indicators |
|-------|----------------|------------|
| Planning | Backlog | Issues being created, no work started |
| Active | In Progress | At least one issue in progress |
| Closing | In Review | All issues done or in review |
| Done | Done | All issues closed, epic closed |

## Completing an Epic

### Pre-Completion Checklist

Before closing an epic:

- [ ] All issues in epic are closed
- [ ] Success criteria in epic are checked off
- [ ] Any dependent epics are updated
- [ ] Initiative (if any) is notified

### Close the Epic

```bash
# Final progress update
gh issue comment [EPIC_NUMBER] --body "## Epic Complete 🎉

**All issues resolved:**
- [x] #100 - Research spike
- [x] #101 - Initial setup
- [x] #102 - Database schema
- [x] #103 - API endpoints

**Success criteria met:**
- [x] Criterion 1
- [x] Criterion 2
- [x] Criterion 3

**Completed:** [DATE]
**Duration:** [X days/weeks]"

# Close the epic
gh issue close [EPIC_NUMBER]

# Update initiative if applicable
gh issue comment [INITIATIVE_NUMBER] --body "## Epic Complete: #[EPIC_NUMBER]

[Epic Name] is now complete. [X] issues resolved.

**Remaining epics:** [List]"
```

## Epic Dependencies

### Documenting Dependencies

In the epic body:

```markdown
## Dependencies

### This Epic Requires
- #[EPIC_A] - [Title] - **Status:** [Done/In Progress]
  - Blocked items in this epic: #101, #102

### This Epic Enables
- #[EPIC_B] - [Title] - Will unblock when this completes
```

### Managing Blocked Issues

When an issue is blocked by another epic:

```bash
gh issue edit [ISSUE_NUMBER] --add-label "blocked"

gh issue comment [ISSUE_NUMBER] --body "**Blocked by:** Epic #[OTHER_EPIC]

Waiting for: #[SPECIFIC_ISSUE] to complete.

Will unblock when: [Condition]"
```

## Epic Without Initiative

For standalone epics (not part of a larger initiative):

```bash
gh issue create \
  --title "[Epic] [NAME]" \
  --label "epic,epic-[SHORT-NAME]" \
  --body "## Epic: [NAME]

## Goal
[What this epic delivers]

## Success Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Issues
[To be created]

## Progress
**Issues:** 0 / 0 complete

---
**Type:** Standalone epic
**Milestone:** [If applicable]"
```

## Example: Dark Mode Epic

### Create Epic

```bash
gh label create "epic-dark-mode" --color "1D76DB" \
  --description "Dark mode theme implementation"

gh issue create \
  --title "[Epic] Dark Mode Support" \
  --label "epic,epic-dark-mode" \
  --milestone "Q1 2026" \
  --body "## Epic: Dark Mode Support

## Goal
Users can toggle between light and dark themes, with preference persistence.

## Success Criteria
- [ ] Theme toggle in settings
- [ ] All components respect theme
- [ ] Preference persists across sessions
- [ ] System preference detection

## Issues

### Ready
- [ ] #201 - Design tokens for dark theme
- [ ] #202 - Theme context provider
- [ ] #203 - Settings toggle UI
- [ ] #204 - Component theme updates
- [ ] #205 - Preference persistence
- [ ] #206 - System preference detection

## Progress
**Issues:** 0 / 6 complete
**Last Updated:** 2025-12-02"
```

### Create Issues

```bash
gh issue create \
  --title "[Feature] Design tokens for dark theme" \
  --label "epic-dark-mode,feature" \
  --body "Part of epic #200: Dark Mode Support

## Description
Create CSS custom properties for dark theme colors.

## Acceptance Criteria
- [ ] Dark theme color palette defined
- [ ] CSS variables for all theme colors
- [ ] Documentation of token usage"
```

## Memory Integration

```bash
mcp__memory__create_entities([{
  "name": "Epic-[NAME]",
  "entityType": "Epic",
  "observations": [
    "Created: [DATE]",
    "Goal: [GOAL]",
    "Issue: #[NUMBER]",
    "Label: epic-[SHORT-NAME]",
    "Status: [Planning/Active/Done]",
    "Issues: [COUNT]",
    "Initiative: #[N] or Standalone"
  ]
}])
```

## Checklist

- [ ] Created epic-specific label
- [ ] Created epic tracking issue
- [ ] **Added epic to project board (VERIFIED with ITEM_ID)**
- [ ] **Set project Status = Backlog or Ready**
- [ ] **Set project Type = Epic**
- [ ] Defined success criteria
- [ ] Documented dependencies
- [ ] Created initial issues with epic label
- [ ] **Added all child issues to project board**
- [ ] **Set Status and Type for all child issues**
- [ ] **Linked children to epic (Epic field if available)**
- [ ] Set milestone (if applicable)
- [ ] Linked to initiative (if applicable)
- [ ] Stored in knowledge graph

**Gate:** Cannot create child issues or begin work without epic and all issues in project board.

**Skill:** `project-board-enforcement`
