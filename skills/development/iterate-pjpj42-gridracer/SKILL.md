---
name: iterate
description: Full development cycle - build, test, play-test, commit
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - AskUserQuestion
  - mcp__automation__screenshot
  - mcp__automation__mouseClick
  - mcp__automation__windowControl
  - mcp__automation__sleep
model: sonnet
---

# Full Development Cycle

Complete iteration: build -> test -> play-test -> commit.

## Workflow

```
Check Current Issue (if any)
     |
     v
  /build -----> Fails? Fix and retry
     |
  Success
     v
  /test ------> Fails? Fix and retry
     |
  Success
     v
/play-test ---> Bug Found? ──> Create Issue (#N)
     |                            |
  No bugs                        v
     |                     Continue or fix later?
     v
Review Changes
     |
     v
Commit with issue reference
     |
     v
Close issue if complete? (#M)
```

## Steps

### 0. Check Current Work

```bash
# Check if on issue branch
BRANCH=$(git branch --show-current)
if [[ "$BRANCH" =~ issue-([0-9]+) ]]; then
    ISSUE_NUM=${BASH_REMATCH[1]}
    echo "🔨 Working on Issue #$ISSUE_NUM"
    gh issue view $ISSUE_NUM --json title,labels,state 2>/dev/null || echo "  (Issue details unavailable)"
    echo ""
fi
```

### 1. Build
Run the build skill. If it fails, analyze errors, fix code, retry.

### 2. Unit Tests
Run the test skill. If tests fail, analyze, fix, retry from build.

### 3. Play Test (Recommended)

Run the play-test skill.

**If bugs found**:
```
🐛 Bug Found: [Description from play-test]

Create GitHub issue for this bug? [Y/n]
```

If yes:
```bash
# Auto-create issue with bug details
gh issue create \
  --title "BUG: [Short description]" \
  --template bug_report.md \
  --label "bug,play-test-found" \
  --body "$(cat <<'EOF'
[Bug details from play-test output]

**Severity**: [Detected severity]

**Steps to Reproduce**: [From play-test]

**Expected Behavior**: [What should happen]

**Actual Behavior**: [What happened]

**Game State**: [Position, velocity, etc.]

---
Found during /iterate play-testing
EOF
)"
```

Output: "✓ Issue #N created. Fix now or continue? [fix/continue]"

- If "fix": Stop here, work on issue, retry /iterate later
- If "continue": Proceed to commit (will reference issue)

**If no bugs**: Continue to commit step.

### 4. Commit

If all steps pass:

```bash
git status
git diff --stat

# Check if working on issue
BRANCH=$(git branch --show-current)
if [[ "$BRANCH" =~ issue-([0-9]+) ]]; then
    ISSUE_NUM=${BASH_REMATCH[1]}
    echo ""
    echo "💡 Working on Issue #$ISSUE_NUM"
    echo ""
    echo "Is this commit completing the issue? [Y/n]"
    # If yes: use "Fixes #$ISSUE_NUM"
    # If no: use "Refs #$ISSUE_NUM"
fi

git add -A
git commit -m "$(cat <<'EOF'
Description of changes

- Detail 1
- Detail 2

[Fixes #N if closing issue, or Refs #N if work continues]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"

# If issue was marked as fixed, close it
if [[ ! -z "$ISSUE_NUM" ]] && [[ "$CLOSES_ISSUE" == "yes" ]]; then
    gh issue comment $ISSUE_NUM --body "✅ Fixed in commit $(git rev-parse --short HEAD)"
    gh issue close $ISSUE_NUM
    echo "✓ Issue #$ISSUE_NUM closed"
fi
```

## Commit Message Guidelines
- Start with verb: Add, Fix, Update, Refactor, Remove
- Be specific: "Add ground plane collision" not "Update game"
- Keep first line under 72 characters
- Reference issues:
  - `Fixes #N` - Auto-closes issue on merge
  - `Refs #N` - Links without closing

## Examples

```
Fix wall collision detection (Fixes #47)

- Check all cells in Bresenham path
- Add unit test for corner collision
- Verified with play-testing

Fixes #47

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

```
Add lap counter display (Refs #42)

- Show current lap in HUD
- Update on finish line cross
- Still need: total laps, styling

Refs #42

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```
