---
name: standup
description: |
  USE WHEN: returning to a project after time away (1 day to 30 days), needing project status briefing, understanding where work left off, determining next steps.
  DO NOT USE WHEN: actively working on a known task, not in a git repository, or when specific file/code questions are asked.
license: MIT
---

This skill orients you to a project's current state regardless of how long you've been away. Whether it's the next morning or a month later, it answers: What is this project? Where did we leave off? What should I work on next?

## Standup Thinking

Before generating the briefing, determine the context:

- **Time gap detection**: Check when the last commit was. If recent (< 3 days), focus on continuation. If stale (> 7 days), provide more project context and recap.
- **Project understanding**: What does this codebase do? Read package.json, README, or main entry points to summarize purpose.
- **Current state**: What branch are we on? Any uncommitted work? What was the last meaningful change?
- **Objectives**: What are the open issues, TODOs, or documented next steps? What was the trajectory before the pause?

**CRITICAL**: Adapt depth to the gap. After 1 day: brief status update. After 30 days: re-orient to the project itself, then status. Always end with clear next steps.

## Information Gathering

### Step 1: Determine Time Gap and Project Context
```bash
# When was the last commit? This determines briefing depth
git log -1 --format="%cr (%ci)"

# Project identity - what is this?
cat package.json 2>/dev/null | head -20 || cat Cargo.toml 2>/dev/null | head -15 || cat setup.py 2>/dev/null | head -15 || cat go.mod 2>/dev/null | head -10 || ls -la

# README snippet for project purpose
head -50 README.md 2>/dev/null || head -50 readme.md 2>/dev/null
```

### Step 2: Recent History (adaptive depth)
```bash
# Last 20 commits with dates - scan for activity patterns
git log --oneline --all -20 --format="%h %cr - %s"

# What branches exist and when were they touched?
git for-each-ref --sort=-committerdate --count=8 refs/heads/ --format='%(refname:short) (%(committerdate:relative)) - %(subject)'

# Current branch status
git status -sb

# Any uncommitted work?
git diff --stat
git diff --cached --stat

# Stashed work waiting to be resumed?
git stash list
```

### Step 3: Project Objectives and Next Steps
```bash
# Open issues (if GitHub)
gh issue list --state open --limit 8 2>/dev/null

# Open PRs
gh pr list --state open --limit 5 2>/dev/null

# Look for TODO tracking files
cat TODO.md 2>/dev/null | head -30 || cat ROADMAP.md 2>/dev/null | head -30
```

Also scan for:
- `docs/handoffs/` - session handoff documents
- `CHANGELOG.md` - recent version changes
- TODO/FIXME comments in recently modified files

### Step 4: Codebase Structure (for longer gaps)
If last commit > 7 days ago, also provide:
```bash
# High-level structure
find . -type f -name "*.ts" -o -name "*.js" -o -name "*.py" -o -name "*.go" -o -name "*.rs" 2>/dev/null | head -30 | xargs dirname | sort -u | head -15

# Key entry points
ls -la src/ 2>/dev/null || ls -la lib/ 2>/dev/null || ls -la app/ 2>/dev/null
```

## Synthesis Guidelines

Focus on:
- **Orientation first**: Before diving into status, ensure the user knows what this project IS and DOES. Don't assume context.
- **Trajectory over history**: What direction was the project heading? Feature development? Bug fixes? Refactoring? This informs next steps.
- **Incomplete work priority**: Uncommitted changes, WIP branches, and draft PRs are the highest priority to surface—this is interrupted work.
- **Actionable next step**: Always conclude with ONE clear recommendation for what to do first.

NEVER assume the user remembers project context after a long gap, dump raw commit logs without synthesis, skip the "what should I do next" recommendation, bury blockers or broken state below routine updates, or provide a briefing longer than 2 screens of content.

## Output Format

Adapt structure based on time gap:

### For Short Gaps (< 3 days since last commit)
```markdown
## Quick Status: [Project Name]
*Last activity: [X ago]*

### Where We Left Off
[Brief: what was the last work session focused on?]

### Current State
- Branch: `[branch]` [ahead/behind remote status]
- Uncommitted: [Y/N - brief description if yes]
- Open PRs: [count and status]

### Next Up
**[Recommended action]**: [Why and how to start]

### Also Pending
- [ ] [Other open item]
- [ ] [Other open item]
```

### For Longer Gaps (> 7 days since last commit)
```markdown
## Project Briefing: [Project Name]
*Last activity: [X ago] | Re-orienting you to this codebase*

### What This Project Is
[2-3 sentences: purpose, tech stack, current state of development]

### Recent History
[Summary of last 3-5 meaningful changes/work items, not individual commits]
- **[Work item]**: [What was done]
- **[Work item]**: [What was done]

### Current State
- Active branch: `[branch]`
- Uncommitted work: [Description if any]
- Open PRs: [List with status]
- Open issues: [Top 3-5 by priority]

### Where This Was Heading
[What was the development trajectory? What feature/goal was in progress?]

### Recommended Next Step
**[Single action]**: [Why this is the priority and specific first action to take]

### Quick Reference
- Entry point: `[main file]`
- Run locally: `[command]`
- Run tests: `[command]`
```

## Interaction Pattern

After presenting the briefing, offer:

```
Ready to dive in? I can:
- Show the diff for uncommitted changes
- Explain what [specific recent change] was about
- Help pick up where [incomplete work] left off
- Give a deeper tour of [area of codebase]
```
