---
name: work-tracking
description: GitHub issue and project board workflow for tracking work. Use when creating issues, updating issue status, checking project board state, assigning milestones, adding labels, or when the user mentions tracking work, creating tasks, filing bugs, feature requests, project board, milestones, or issue management. Also use when the user asks to clean up, triage, or organize existing issues.
user-invocable: false
---

# Work Tracking

This project tracks work through GitHub Issues on a project board. Every issue should have a type label, belong to a milestone when it's part of a project, and appear on the project board.

## Project Board

The project board is a Kanban with three columns:

- **Todo** — work that's planned but not started
- **In Progress** — actively being worked on (should have a linked PR)
- **Done** — completed and merged

Board coordinates for `gh` commands:

- Owner: `QingqiShi`
- Project number: `3`

## Labels

Labels indicate the **type of change**, not the project or area. Use exactly one type label per issue.

| Label      | Purpose                                | Commit type |
| ---------- | -------------------------------------- | ----------- |
| `bug`      | Something is broken                    | `fix`       |
| `feature`  | New functionality                      | `feat`      |
| `refactor` | Code restructuring, no behavior change | `refactor`  |
| `perf`     | Performance improvement                | `perf`      |
| `docs`     | Documentation only                     | `docs`      |
| `chore`    | Maintenance, cleanup, dependencies     | `chore`     |
| `ci`       | CI/CD pipeline changes                 | `ci`        |
| `test`     | Testing infrastructure                 | `test`      |

The "Commit type" column shows how the label maps to the prefix used in commit messages and PR titles (via the `raise-pr` skill). This keeps issue categorization and commit conventions aligned — a `feature` issue results in a `feat:` PR.

Dependabot labels (`dependencies`, `javascript`, `github_actions`) are auto-applied and separate from this scheme.

## Milestones

Milestones represent **projects** — a body of related work toward a goal. When a project is large, break it into sequential phases.

**Naming:**

- Single-phase project: `Project Name`
- Multi-phase project: `Project Name: Phase N - Description`

**Example:** The AI overhaul project uses phases:

- `AI Overhaul: Phase 1 - Chat`
- `AI Overhaul: Phase 2 - Search`
- `AI Overhaul: Phase 3 - Rich UI`

When creating an issue, always communicate the milestone decision to the user — even when it seems obvious. The user may have context you don't (e.g., a new project they're about to start, or a bug that's actually blocking a specific phase). If the work clearly fits an existing milestone, say which one and why. If it doesn't fit any existing milestone, say so and ask whether to create a new one or leave it unassigned. Never silently omit the milestone.

## Creating an Issue

When creating an issue, always include the type label and add it to the project board. Include a milestone if the work belongs to a project.

Before using a label, verify it exists with `gh label list`. If the label doesn't exist yet, create it:

```bash
gh label create "<label-name>" --description "<purpose>" --color "<hex>"
```

Then create the issue and add it to the board:

```bash
# 1. Create the issue
gh issue create \
  --title "<title>" \
  --body "<description>" \
  --label "<type-label>" \
  --milestone "<Milestone Name>"

# 2. Add to the project board (use the issue URL from step 1)
gh project item-add 3 --owner QingqiShi --url <issue-url>
```

If the milestone flag fails because the milestone doesn't exist yet, create it first:

```bash
gh api repos/QingqiShi/shiqingqi.com/milestones -f title="<Milestone Name>" -f description="<Brief description>"
```

## Checking Project Status

```bash
# Board overview — all items with status
gh project item-list 3 --owner QingqiShi --format json

# Open milestones and progress
gh api repos/QingqiShi/shiqingqi.com/milestones --jq '.[] | {title, open_issues, closed_issues}'

# Issues for a specific milestone
gh issue list --milestone "<Milestone Name>"
```

## Updating Issue Status

When starting work on an issue, update the project board to reflect "In Progress". When the linked PR merges, update to "Done".

To update a project item's status, you need the item's node ID and the status field's option IDs. Look these up dynamically:

```bash
# Get the project's item list with node IDs
gh project item-list 3 --owner QingqiShi --format json

# Get field IDs and status option IDs
gh project field-list 3 --owner QingqiShi --format json
```

Then update:

```bash
gh project item-edit \
  --project-id <project-node-id> \
  --id <item-node-id> \
  --field-id <status-field-id> \
  --single-select-option-id <status-option-id>
```
