---
name: finish-the-day
description: End-of-day wrap up - analyzes all work done, creates detailed daily update log, commits all changes, and pushes to remote. Use when user says "finish the day", "end of day", "wrap up", or at end of work session.
---

# Finish the Day - Universal End-of-Day Wrap Up

This skill performs a comprehensive end-of-day wrap up for the **current working directory**. It analyzes all work done, creates a detailed log, commits changes, and pushes to the remote repository. Works on any project.

## What This Skill Does

1. **Analyze Today's Work**
   - Reviews all commits made today
   - Identifies all modified, added, and deleted files
   - Calculates lines added/removed
   - Summarizes changes by category

2. **Create Daily Update Log**
   - Generates comprehensive markdown documentation
   - Organized by feature/area of work
   - Includes code snippets for key changes
   - Documents technical decisions and notes

3. **Commit All Changes**
   - Stages all uncommitted changes
   - Creates detailed commit message
   - Follows conventional commit format

4. **Push to Remote**
   - Pushes all commits to remote repository
   - Reports sync status

## Execution Steps

### Step 1: Gather Information

Collect all data about today's work:

```bash
# Get today's date
date +%Y-%m-%d

# Get project name from current directory or package.json
basename $(pwd)

# Check git status for uncommitted changes
git status

# Get diff stats for uncommitted changes
git diff --stat

# Get today's commits (commits from today)
git log --since="midnight" --oneline

# Get detailed changes from today's commits
git log --since="midnight" --stat

# Get all files changed today (committed + uncommitted)
git diff --name-only HEAD~10 2>/dev/null || git diff --name-only

# Count lines changed
git diff --shortstat
```

### Step 2: Analyze Changes

For each changed file:
1. **Read the file** to understand what was implemented
2. **Categorize changes** by type:
   - New features
   - Bug fixes
   - Refactoring
   - Documentation
   - Configuration
   - Tests
3. **Identify key components** created or modified
4. **Note any breaking changes**

### Step 3: Determine Daily Updates Location

Check for existing daily updates folder:

```bash
# Common locations to check (in order of preference)
# 1. Daily-updates in parent directory (for monorepos)
# 2. docs/daily-updates in project
# 3. daily-updates in project root
# 4. Create in project root if none exist

ls -d ../Daily-updates 2>/dev/null || \
ls -d ./docs/daily-updates 2>/dev/null || \
ls -d ./daily-updates 2>/dev/null || \
echo "Will create ./daily-updates"
```

If no daily updates folder exists, ask the user where to create the log or create `./daily-updates/` in the project root.

### Step 4: Create Daily Update Log

Generate a markdown file with the following structure:

```markdown
# Daily Development Update - [DATE]

## Overview
[Brief summary of what was accomplished]

---

## 1. [Feature/Area Name]

### [Sub-feature]
- Description of changes
- Key implementation details
- Files affected

### Code Changes
[Relevant code snippets or interface definitions]

---

## 2. [Next Feature/Area]
...

---

## Files Modified

| File | Changes |
|------|---------|
| path/to/file | Description |

## Files Created

| File | Lines | Description |
|------|-------|-------------|
| path/to/file | XXX | Description |

---

## Technical Notes
- Important decisions made
- Dependencies added
- Configuration changes

---

## Next Steps / Considerations
- Pending work
- Future improvements
- Issues to address
```

### Step 5: Commit Changes

Stage and commit all changes:

```bash
# Stage all changes including untracked files
git add -A

# Show what will be committed
git status

# Create commit with detailed message
git commit -m "$(cat <<'EOF'
[Type]: Brief description

Detailed changes:
- Item 1
- Item 2
- Item 3

Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### Step 6: Push to Remote

```bash
# Push all commits
git push

# Report final status
git log --oneline -3
```

## Daily Log Format Guidelines

### File Naming
- Format: `YYYY-MM-DD-daily-update.md`
- Example: `2024-12-23-daily-update.md`

### Content Guidelines
1. **Be specific** - Include actual file names, function names, component names
2. **Show code** - Include interface definitions, key function signatures
3. **Document decisions** - Note why certain approaches were chosen
4. **List next steps** - Help future-you know where to continue

### Categories to Consider
- **UI/UX Changes** - Visual updates, layout changes, styling
- **New Features** - New functionality added
- **Bug Fixes** - Issues resolved
- **Refactoring** - Code improvements without functionality changes
- **API Changes** - Backend, endpoints, data structures
- **Configuration** - Build, deployment, environment changes
- **Documentation** - README, comments, docs
- **Tests** - New or updated tests
- **Dependencies** - Added, removed, or updated packages

## Tool Usage

This skill uses:
- `Bash` - For git operations and file system checks
- `Glob` - To find changed files by pattern
- `Read` - To read file contents for analysis
- `Write` - To create the daily update log
- `Task` with `Explore` agent - For deep analysis if needed

## Important Notes

- **Works on current directory** - No hardcoded paths
- **Adapts to any project** - Detects project structure automatically
- **Preserves existing logs** - Adds new log, doesn't overwrite
- **Safe git operations** - Never force pushes or destructive operations
- **Asks before creating folders** - Confirms daily-updates location with user

## Activation Triggers

This skill activates when user says:
- "finish the day"
- "end of day"
- "wrap up"
- "wrap up the day"
- "daily wrap up"
- "create daily update"
- "commit and push everything"
- "end session"

## Example Output

After running this skill, you'll have:

1. **Daily update log** at `[project]/daily-updates/YYYY-MM-DD-daily-update.md`
2. **Git commit** with detailed message summarizing all changes
3. **Pushed to remote** - All work synced to remote repository
4. **Summary report** showing:
   - Files changed (X modified, Y created, Z deleted)
   - Lines changed (+XXX, -YYY)
   - Commits pushed (X commits)
   - Daily log location
