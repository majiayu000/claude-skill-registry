---
name: clean-branches
description: >
  Use when user says "clean up branches", "delete merged branches",
  "prune stale branches", "git branch cleanup", "remove old branches",
  or wants to safely remove merged or stale git branches.
model: claude-sonnet-4-5
argument-hint: [branch-pattern] - optional pattern to filter branches
allowed-tools:
  - Bash(git:*)
  - AskUserQuestion
---

# Clean Git Branches

Safely remove merged and stale git branches with confirmation.

## Process

**0. Parse arguments**
If `$ARGUMENTS` provided, use as branch pattern filter (e.g., `feature/*`).

**1. Fetch latest state**
```bash
git fetch --all --prune
```

**2. Identify candidates**

Find merged branches:
```bash
git branch --merged main | grep -v "^\*\|main\|master\|develop"
```

Find stale branches (no commits in 30+ days):
```bash
git for-each-ref --sort=-committerdate --format='%(refname:short) %(committerdate:relative)' refs/heads/ | while read branch date; do
  if [[ "$date" == *"months"* ]] || [[ "$date" == *"year"* ]]; then
    echo "$branch ($date)"
  fi
done
```

**3. Categorize and display**

Present findings:
```
MERGED BRANCHES (safe to delete):
- feature/old-feature
- fix/completed-fix

STALE BRANCHES (no recent commits):
- experiment/abandoned (3 months ago)
- wip/forgotten (6 months ago)

PROTECTED (never delete):
- main, master, develop
```

**4. Confirm before deletion**

Use AskUserQuestion:
- "Delete all merged branches?"
- "Delete specific stale branches?" (list options)
- "Skip and keep all?"

**5. Execute deletion**

Local only (safe):
```bash
git branch -d <branch-name>
```

If user explicitly requests remote cleanup:
```bash
git push origin --delete <branch-name>
```

## Safety Rules

- Never delete: main, master, develop, release/*
- Always confirm before any deletion
- Use `-d` (safe delete) not `-D` (force)
- Show what will be deleted before acting
- Remote deletion requires explicit confirmation

## Output

Summary:
- Branches deleted (local)
- Branches deleted (remote, if requested)
- Branches kept
- Any errors encountered
