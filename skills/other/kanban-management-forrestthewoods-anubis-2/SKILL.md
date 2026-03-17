---
name: kanban-management
description: Manages the Anubis Issue Tracker GitHub project board. Use when you need to organize issues by difficulty/status, move issues through workflow stages, or generate board status reports.
---

# Kanban Project Management

## Project Board

The **Anubis Issue Tracker** project board is already created and configured:
- **Project URL:** https://github.com/users/forrestthewoods/projects/8
- **Project Number:** 8
- **Owner:** forrestthewoods

**Important:** Do NOT create a new project board. Always use project #8.

## Board Status Workflow

The project board uses these seven status columns:

| Status | Description |
|--------|-------------|
| **Backlog** | Future ideas or deferred work; not ready for action yet |
| **Triage** | New issues not yet added to the project board |
| **Needs Agent Review** | Issues ready for agent to review and categorize |
| **Needs Human Review** | Agent has questions; waiting for human clarification |
| **Ready to Implement** | Agent reviewed, wrote plan, no questions remaining |
| **Needs Code Review** | Implementation in progress (has active branch) |
| **Done** | Closed and completed (automatic via GitHub) |

**Important:** Issues in **Backlog** should be **completely ignored** by all skills. These are tasks that have been captured so they won't be forgotten, but are not ready for action. They will be moved to Triage or Needs Agent Review when they are ready to be worked on.

## Workflow Overview

1. **New issues** are created in GitHub Issues
2. Issues not in the project are placed in **Triage**
3. Issues move to **Needs Agent Review** for agent processing
4. Agent reviews each issue:
   - Labels the issue as `difficulty: easy`, `difficulty: medium`, or `difficulty: hard`
   - If clarification needed → post questions as comment → move to **Needs Human Review**
   - If no questions → write detailed implementation plan as comment → move to **Ready to Implement**
5. When implementation begins, agent creates branch using the branch naming convention
6. Issues with active branches are detected and moved to **Needs Code Review**
7. When issue is closed, GitHub automatically moves it to **Done**

## Purpose

This skill helps manage the existing project board by:
1. Adding new issues to the board
2. Moving issues through workflow stages
3. Organizing issues by difficulty labels
4. Generating board status reports
5. Maintaining board hygiene

## Instructions

### Step 1: View Current Board State

```bash
# List all items on the project board
gh project item-list 8 --owner forrestthewoods --format json

# View project details
gh project view 8 --owner forrestthewoods --format json
```

### Step 2: Add New Issues to Board

When new issues are created, add them to the board:

```bash
# Add a single issue
gh project item-add 8 --owner forrestthewoods --url https://github.com/forrestthewoods/anubis/issues/<number>

# Add all open issues not yet on board
gh issue list --state open --json url -q '.[].url' | while read url; do
  gh project item-add 8 --owner forrestthewoods --url "$url" 2>/dev/null
done
```

### Step 3: Move Issues Through Stages

Update issue status based on progress:

```bash
# Get project and field IDs
gh project view 8 --owner forrestthewoods --format json

# Get item ID for specific issue
gh project item-list 8 --owner forrestthewoods --format json | jq '.items[] | select(.content.number == <issue-number>)'

# Update status
gh project item-edit --project-id <project-id> --id <item-id> --field-id <status-field-id> --single-select-option-id <option-id>
```

**Status Transition Rules:**

| From | To | Trigger |
|------|-----|---------|
| Triage | Needs Agent Review | Issue added to project board |
| Needs Agent Review | Needs Human Review | Agent posts clarifying questions |
| Needs Agent Review | Ready to Implement | Agent writes implementation plan |
| Needs Human Review | Needs Agent Review | Human responds to questions |
| Ready to Implement | Needs Code Review | Agent creates implementation branch |
| Needs Code Review | Done | PR merged and issue closed |

### Step 4: Manage Difficulty Labels

Ensure issues have appropriate difficulty labels:

```bash
# Create difficulty labels (if not exist)
gh label create "difficulty: easy" --color "0E8A16" --description "Simple change, good first issue" --force
gh label create "difficulty: medium" --color "FBCA04" --description "Moderate complexity" --force
gh label create "difficulty: hard" --color "D93F0B" --description "Complex, requires significant effort" --force

# Add label to issue
gh issue edit <number> --add-label "difficulty: easy|medium|hard"
```

### Step 5: Generate Board Status Report

```markdown
## Anubis Issue Tracker - Board Status

**Project:** https://github.com/users/forrestthewoods/projects/8

### Summary
- **Total Issues:** 22
- **Triage:** 2
- **Needs Agent Review:** 5
- **Needs Human Review:** 3
- **Ready to Implement:** 8
- **Needs Code Review:** 2
- **Done:** 2

### By Difficulty

| Difficulty | Triage | Agent Review | Human Review | Ready to Impl | Code Review | Done |
|------------|--------|--------------|--------------|---------------|-------------|------|
| Easy       | 0      | 1            | 1            | 3             | 1           | 1    |
| Medium     | 1      | 2            | 1            | 3             | 1           | 1    |
| Hard       | 0      | 2            | 1            | 2             | 0           | 0    |
| Unlabeled  | 1      | 0            | 0            | 0             | 0           | 0    |

### Ready to Implement (Prioritized)
These issues have plans and are ready for work:

**Easy (Quick Wins):**
1. #10 - Fix typo in README
2. #11 - Add --help examples

**Medium:**
1. #18 - Add user preferences

**Hard:**
1. #22 - Refactor build system

### Needs Human Review
These need human responses before agent can continue:
- #4 - Asked about reproduction steps (3 days ago)
- #9 - Asked about expected behavior (1 day ago)

### Needs Code Review
Implementation in progress (has active branch):
- #25 - Parallel builds (branch: claude/issue-25-parallel-builds)
- #30 - Add caching (branch: claude/issue-30-add-caching)

### Stale Items
Items that haven't been updated in 14+ days:
- #8 - In "Ready to Implement" since Dec 1
- #12 - In "Needs Human Review" since Nov 28 (may need follow-up)
```

### Step 6: Board Hygiene Tasks

**Weekly cleanup checklist:**

1. **Check for orphaned issues:**
   ```bash
   # Find open issues not on board
   gh issue list --state open --json number,title | jq -r '.[] | "#\(.number) - \(.title)"'
   ```

2. **Archive completed items older than 30 days:**
   - Items in "Done" status can be archived to keep board clean

3. **Flag stale "Needs Code Review" items:**
   - Issues in "Needs Code Review" for more than 14 days may have stalled PRs

4. **Verify labels match board status:**
   - All issues should have a difficulty label once they leave "Triage"

5. **Check for issues needing triage:**
   - New issues should be moved from "Triage" to "Needs Agent Review" promptly

6. **Check for stale "Needs Human Review":**
   - Issues waiting for human response for more than 7 days may need follow-up

7. **Detect issues with active branches:**
   ```bash
   # List all remote branches that may correspond to issues
   git ls-remote --heads origin | grep -E 'claude/issue-|issue-'
   ```
   - Issues with active branches should be in "Needs Code Review"

## Automation Notes

The project board has automated workflows that handle:
- Moving items to "Done" when issues are closed
- Moving items when issues are reopened

These automations run automatically. Manual/agent status updates are needed for:
- Moving from "Triage" to "Needs Agent Review"
- Agent review decisions (to "Needs Human Review" or "Ready to Implement")
- Detecting active branches and moving to "Needs Code Review"

## Guidelines

- Keep the board focused on actionable items
- Update status when actual progress changes
- Don't let items sit in "In-progress" indefinitely
- Review stale items weekly
- Use consistent labeling between issues and board
- Prioritize items in "Triage" status quickly
- Ensure all open issues are on the board

## Quick Reference Commands

```bash
# View board
gh project view 8 --owner forrestthewoods --web

# List all items
gh project item-list 8 --owner forrestthewoods

# Add issue to board
gh project item-add 8 --owner forrestthewoods --url <issue-url>

# List open issues
gh issue list --state open

# View specific issue
gh issue view <number>

# Edit issue labels
gh issue edit <number> --add-label "difficulty: easy"
```
