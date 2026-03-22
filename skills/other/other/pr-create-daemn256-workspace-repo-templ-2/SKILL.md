---
name: pr-create
description: Create a pull request with title, body, labels, and template
---

# PR Create

Uses **Orchestrator**. Create a pull request with appropriate title, template, labels, and description.

**Prerequisites:** Branch exists with commits, changes pushed to remote, verification passed (build, tests)

---

## Phase 1: Determine Configuration

### PR Setup

1. Determine PR title from branch type: `<type>(<scope>): <description>`
2. Select template based on work type:

| Work Type     | Template        |
| ------------- | --------------- |
| Features      | `pr.md`         |
| Bug fixes     | `pr.md`         |
| Documentation | `pr.md`         |
| Maintenance   | `pr.md`         |
| Hotfixes      | `pr-hotfix.md`  |
| Releases      | `pr-release.md` |

3. Determine labels (type, topic, area)
4. Determine target branch:

| Scenario           | Target            |
| ------------------ | ----------------- |
| Standalone work    | `main`            |
| Part of epic/phase | Epic/phase branch |
| Hotfix             | `main`            |

5. Note merge method for reviewer context (default: merge commit; read `project.merge-method` from `workspace.config.yaml`)

---

## Phase 2: Compose PR Body

### Write Description

1. Write summary (what and why)
2. List scope (files changed, areas affected)
3. Document validation (build passes, tests pass)
4. Add links (closes issue, related ADRs)
5. Fill in the selected template

### Output

```markdown
## Context Anchors

- **Issue:** #<number> - <title>
- **Branch:** `<branch>` → `<target>`
- **Phase:** 2 — Compose PR Body

## PR Configuration

| Property     | Value                            |
| ------------ | -------------------------------- |
| Title        | `<type>(<scope>): <description>` |
| Template     | `<template>.md`                  |
| Target       | `<target-branch>`                |
| Merge method | <method from config>             |
| Labels       | `type:...`, `topic:...`          |

## PR Body Preview

<full body content>

## Next Step

Awaiting approval to create PR.

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP.** Do not create PR until human explicitly approves:

- PR title and labels
- Target branch
- PR body content

---

## Phase 3: Create and Report

### Execute PR Creation

1. Write PR body to `.tmp/scratch/pr-body.md`
2. Execute the forge's PR creation operation with:
   - **Base:** target branch (from Phase 1)
   - **Head:** feature branch
   - **Title:** `<type>(<scope>): <description>`
   - **Body:** from `.tmp/scratch/pr-body.md`
   - **Labels:** from Phase 1
3. Update board status to **In Review** for the linked issue
4. Report PR number and URL

### Board Integration

Read `workspace.config.yaml` for board field IDs.
Set issue status to In Review (`board.status_options.in-review.option_id`).

### Output

```markdown
## Context Anchors

- **PR:** #<pr-number> - <title>
- **Issue:** #<issue-number>
- **Status:** Open, awaiting review

## Next Step

PR created. Awaiting review.

**Approval Required:** No
```

---

## Error Handling

| Error                   | Recovery                    |
| ----------------------- | --------------------------- |
| Branch not pushed       | Push first, then retry      |
| Build/tests not passing | Fix issues before PR        |
| Missing issue link      | Confirm issue number        |
| Forge not authenticated | Check authentication status |
