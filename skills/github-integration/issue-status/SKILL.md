---
name: issue-status
description: Show current work status
allowed-tools:
  - Bash
model: haiku
---

# Issue Status

Show current work-in-progress and recent issue activity.

## Usage

```
/issue-status
```

## Steps

### 1. Check Current Branch

```bash
BRANCH=$(git branch --show-current)

# Extract issue number if on issue branch
if [[ "$BRANCH" =~ issue-([0-9]+) ]]; then
    ISSUE_NUM=${BASH_REMATCH[1]}
    echo "🔨 Currently Working On:"
    gh issue view $ISSUE_NUM --json number,title,labels

    # Show last commit time
    LAST_COMMIT=$(git log -1 --format="%ar")
    echo "  Last commit: $LAST_COMMIT"
fi
```

### 2. Show Recent Commits with Issue References

```bash
echo ""
echo "📝 Recent Commits:"
git log --oneline -10 | grep -E '#[0-9]+'
```

### 3. Show Open Issues

```bash
echo ""
echo "📊 Open Issues:"
gh issue list --limit 10
```

### 4. Show Recently Closed Issues

```bash
echo ""
echo "✅ Recently Closed:"
gh issue list --state closed --limit 5
```

### 5. Show Project Stats

```bash
echo ""
echo "📈 Project Stats:"

# Count by type
BUGS=$(gh issue list --label bug --json number --jq 'length')
FEATURES=$(gh issue list --label feature --json number --jq 'length')
TASKS=$(gh issue list --label task --json number --jq 'length')
TOTAL_OPEN=$(gh issue list --json number --jq 'length')

echo "  Open: $TOTAL_OPEN issues ($BUGS bugs, $FEATURES features, $TASKS tasks)"

# Closed this week
WEEK_AGO=$(date -v-7d +%Y-%m-%d)
CLOSED_WEEK=$(gh issue list --state closed --search "closed:>=$WEEK_AGO" --json number --jq 'length')
echo "  Closed this week: $CLOSED_WEEK issues"
```

## Example Output

```
🔨 Currently Working On:
  Issue #47: Racer moves through walls
  Branch: issue-47-wall-collision
  Labels: bug, collision-detection, play-test-found
  Last commit: 30 minutes ago

📝 Recent Commits:
  abc1234 Fix wall collision detection (Refs #47)
  def5678 Add Bresenham line tests (Refs #47)

📊 Open Issues:
#52  Racer respawns at wrong position         bug, game-logic
#50  Add lap counting                         feature, game-logic, ui
#48  Optimize SceneKit rendering              task, scenekit, performance

📈 Recently Closed:
#47  Racer moves through walls               (closed 2 hours ago)
#45  Add velocity display                    (closed 1 day ago)

📈 Project Stats:
  Open: 8 issues (3 bugs, 4 features, 1 task)
  Closed this week: 5 issues
```

## Use Cases

**Daily standup check**:
```
/issue-status
→ See what you're working on and what needs attention
```

**Before starting new work**:
```
/issue-status
→ Check current branch, decide if should finish current issue first
```

**Project progress review**:
```
/issue-status
→ See velocity, open/closed ratio
```

## Notes

- Works without issue branch (shows general project status)
- Useful for context switching between issues
- Shows only summary; use `/issues` for full issue list
- Stats require gh CLI and jq (JSON processor)
