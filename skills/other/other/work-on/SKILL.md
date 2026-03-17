---
name: work-on
description: Start work on GitHub issue
argument-hint: "[issue-number]"
allowed-tools:
  - Bash
  - Read
  - Grep
  - AskUserQuestion
model: sonnet
---

# Work On Issue

Begin work on a GitHub issue by fetching context and setting up.

## Usage

```
/work-on 42
/work-on 47
```

## Steps

### 1. Fetch Issue Details

```bash
gh issue view 42 --json number,title,body,labels,milestone,state
```

### 2. Display Context

Format and display issue information:

```
📋 Issue #42: Add lap counter
Labels: feature, ui, game-logic
Milestone: v1.0
State: OPEN

Description:
[Issue body content - formatted for readability]

Acceptance Criteria:
[Extract checklist items if present]
```

### 3. Add Work Comment

Notify on the issue that work has started:

```bash
gh issue comment 42 --body "🔨 Starting work on this issue

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

### 4. Suggest Next Steps

Based on issue labels, suggest appropriate action:

**If labeled `bug`**:
```
Suggested next step: /debug "issue title here"

This will help investigate the root cause before implementing a fix.
```

**If labeled `feature`**:
```
Suggested next step: /feature "feature name"

This will check the design doc and plan implementation.
```

**If labeled `task`**:
```
Suggested next step: Read relevant files and plan approach

Files to review:
[List files mentioned in issue body or inferred from labels]
```

### 5. Optional: Create Branch

Ask user if they want to create a dedicated branch:

```
Create branch for this issue? [Y/n]

Suggested branch name: issue-42-lap-counter
```

If yes:
```bash
git checkout -b issue-42-lap-counter
```

## Label-Based Suggestions

```
bug + collision-detection:
  → /debug "title"
  → Read: GridRacer/CollisionDetection.swift

bug + scenekit:
  → /debug "title"
  → Read: GridRacer/GameViewController.swift

bug + game-logic:
  → /debug "title"
  → Read: GridRacer/GameState.swift

feature + any:
  → /feature "title"
  → Read: docs/GridRacer Concept.md

task + testing:
  → Read: GridRacerTests/
  → Review existing test patterns

task + performance:
  → Read: .claude/rules/performance.md
  → Profile current implementation
```

## Example Workflow

```
User: /work-on 47

Claude fetches issue:
📋 Issue #47: Racer moves through walls
Labels: bug, play-test-found, collision-detection
State: OPEN

Description:
During play-testing, racer was able to move through walls at high velocity.

Steps to Reproduce:
1. Accelerate to velocity (3, 2)
2. Select marker that goes diagonally through wall
3. Racer passes through instead of crashing

Expected: Crash detected, life lost, respawn at (0,0)
Actual: Racer passes through wall

Game State:
- Position: (10, 5)
- Velocity: (3, 2)
- Marker selected: (+1, +1)

Adds comment to issue: "🔨 Starting work on this issue"

Suggested next step: /debug "racer moves through walls"

Files to review:
- GridRacer/CollisionDetection.swift
- GridRacer/BresenhamLine.swift

Create branch issue-47-wall-collision? [Y/n]
```

## Branch Naming Convention

Pattern: `issue-{number}-{slug}`

Examples:
- `issue-42-lap-counter`
- `issue-47-wall-collision`
- `issue-50-ai-opponent`

Slug generated from title:
1. Take first 3-4 words
2. Remove special characters
3. Convert to kebab-case
4. Truncate to ~20 chars

## Notes

- Always fetch fresh issue data (don't use cached)
- Comment on issue helps track who's working on what
- Branch creation is optional but recommended for features
- Suggested next steps are guidance, not requirements
- Labels help determine best approach to start work
