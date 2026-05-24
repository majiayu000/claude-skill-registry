---
name: issue-create
description: Create GitHub issue with template
argument-hint: "[title]"
allowed-tools:
  - Bash
  - AskUserQuestion
model: sonnet
---

# Create GitHub Issue

Create new issue with appropriate template and labels.

## Usage

```
/issue-create "Racer moves through walls"
/issue-create "Add AI opponent difficulty levels"
/issue-create "Refactor collision detection"
```

## Steps

### 1. Determine Issue Type

Analyze title for keywords:
- Contains "bug", "crash", "broken", "fix", "error" → **bug** template
- Contains "feature", "add", "implement", "new" → **feature** template
- Contains "refactor", "improve", "update", "optimize" → **task** template
- Default if unclear → Ask user

### 2. Auto-Detect Component Labels

Scan title for component keywords:
- "collision", "bresenham", "path" → add `collision-detection`
- "scenekit", "render", "node", "material" → add `scenekit`
- "game", "state", "player", "move" → add `game-logic`
- "ui", "interface", "button", "display" → add `ui`
- "ai", "opponent", "bot" → add `ai`
- "test", "testing" → add `testing`

### 3. Determine Priority (Optional)

Ask user if priority should be set:
- Critical: Game-breaking, unplayable
- High: Major feature broken
- None: Standard priority

### 4. Create Issue

```bash
# Bug example
gh issue create \
  --title "BUG: Racer moves through walls" \
  --template bug_report.md \
  --label "bug,collision-detection"

# Feature example
gh issue create \
  --title "FEATURE: Add AI opponent" \
  --template feature_request.md \
  --label "feature,ai,game-logic"

# Task example
gh issue create \
  --title "TASK: Refactor collision detection" \
  --template task.md \
  --label "task,collision-detection"
```

### 5. Return Issue Number

Parse output to extract issue number and display:

```
✓ Issue #47 created: "BUG: Racer moves through walls"
Labels: bug, collision-detection
View: gh issue view 47
```

## Type Detection Logic

```
Keywords for BUG:
  - bug, crash, broken, error, fail, fix
  - incorrect, wrong, issue, problem
  - teleport, glitch

Keywords for FEATURE:
  - feature, add, implement, new, create
  - support, enable, allow

Keywords for TASK:
  - refactor, improve, update, optimize
  - clean, reorganize, restructure
  - performance, maintainability
```

## Component Detection Logic

```
collision-detection:
  - collision, bresenham, path, wall, crash

scenekit:
  - scenekit, render, node, material, camera
  - scene, geometry, visual, display

game-logic:
  - game, state, player, move, turn
  - velocity, position, lap, finish

ui:
  - ui, interface, button, menu, hud
  - control, input, display, screen

ai:
  - ai, opponent, bot, computer, difficulty

testing:
  - test, testing, unit, integration, spec
```

## Example Workflows

**Bug Report**:
```
User: /issue-create "Racer teleports through walls at high velocity"

Claude:
- Detected: BUG (keywords: teleport, walls)
- Component: collision-detection (keywords: walls, velocity)
- Template: bug_report.md

Creates issue #47 with:
- Title: "BUG: Racer teleports through walls at high velocity"
- Labels: bug, collision-detection
- Template: bug_report.md
```

**Feature Request**:
```
User: /issue-create "Add AI opponent with multiple difficulty levels"

Claude:
- Detected: FEATURE (keywords: add)
- Components: ai (keywords: AI, opponent, difficulty)
- Template: feature_request.md

Creates issue #48 with:
- Title: "FEATURE: Add AI opponent with multiple difficulty levels"
- Labels: feature, ai
- Template: feature_request.md
```

## Notes

- Issue is created but template sections need manual filling
- User can edit issue on GitHub after creation
- Skills like `/play-test` and `/debug` create fully-filled issues
- For manual creation, this skill just sets up the structure
