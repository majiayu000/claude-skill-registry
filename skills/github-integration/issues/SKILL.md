---
name: issues
description: List and filter GitHub issues
argument-hint: "[filter]"
allowed-tools:
  - Bash
model: haiku
---

# List GitHub Issues

Display open issues with optional filtering.

## Usage

```
/issues              # List all open issues
/issues bug          # Filter by label
/issues feature      # Filter by feature label
/issues milestone:v1.0  # Filter by milestone
```

## Steps

### 1. Parse Arguments

If argument provided:
- Check if it's a milestone filter (contains "milestone:")
- Otherwise treat as label filter

### 2. List Issues

```bash
# Default: list all open issues
gh issue list --limit 50

# With label filter
gh issue list --label "bug" --limit 50

# With milestone filter
gh issue list --milestone "v1.0" --limit 50
```

### 3. Format Output

Display in readable format with:
- Issue number
- Type label (bug/feature/task)
- Title
- Additional labels in parentheses

## Example Output

```
#42  [bug] Racer teleports through walls           (play-test-found, collision-detection)
#38  [feature] Add AI opponent                     (game-logic, ai)
#35  [task] Refactor collision detection           (collision-detection)

3 open issues
```

## Filter Examples

```bash
/issues bug                    # Only bugs
/issues feature                # Only features
/issues play-test-found        # Auto-discovered bugs
/issues collision-detection    # Collision issues
/issues milestone:v1.0         # Issues in v1.0 milestone
```

## Notes

- Uses GitHub CLI (`gh`) which requires authentication
- Shows open issues by default
- For closed issues, users can run: `gh issue list --state closed`
- Labels are color-coded in terminal output
