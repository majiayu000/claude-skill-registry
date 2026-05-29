---
name: pop-next-action
description: "Context-aware recommendation engine that analyzes git status, TypeScript errors, GitHub issues, and technical debt to suggest prioritized next actions. Returns specific popkit commands with explanations of why each is relevant. Use when unsure what to work on next, starting a session, or feeling stuck. Do NOT use when you already know what to do - just proceed with that task directly."
---

# Next Action Recommendation

## Overview

Analyzes current project state and provides prioritized, context-aware recommendations for what to work on next. Returns actionable popkit commands with explanations.

**Core principle:** Don't just list commands - recommend the RIGHT command based on actual project state.

**Trigger:** When user expresses uncertainty ("what should I do", "where to go", "stuck") or runs `/popkit:next`.

## When to Use

Invoke this skill when:

- User asks "what should I do next?"
- User seems stuck or unsure of direction
- User mentions "popkit" and needs guidance
- Starting a new session and need orientation
- Returning to a project after time away

## Analysis Process

### Step 1: Gather Project State

Collect information from multiple sources:

```bash
# Git status
git status --short 2>/dev/null

# Current branch name (for protected branch detection)
current_branch=$(git branch --show-current 2>/dev/null)

# Branch info
git branch -vv 2>/dev/null | head -5

# Recent commits
git log --oneline -5 2>/dev/null

# Fetch remotes to detect research branches
git fetch --all --prune 2>/dev/null
```

**RECORDING: After gathering git state, record initial analysis:**

```python
from popkit_shared.utils.session_recorder import is_recording_enabled, record_reasoning
import subprocess

if is_recording_enabled():
    # Get uncommitted file count
    result = subprocess.run(
        ["git", "status", "--short"],
        capture_output=True,
        text=True
    )
    uncommitted_lines = len([l for l in result.stdout.strip().split('\n') if l])

    # Get current branch name
    branch_result = subprocess.run(
        ["git", "branch", "--show-current"],
        capture_output=True,
        text=True
    )
    current_branch = branch_result.stdout.strip()

    # Check if on protected branch
    PROTECTED_BRANCHES = ["main", "master", "develop", "production"]
    is_protected = current_branch in PROTECTED_BRANCHES

    record_reasoning(
        step="Analyze git status",
        reasoning=f"Checked working directory, branch={current_branch}, protected={is_protected}",
        data={
            "uncommitted_files": uncommitted_lines,
            "current_branch": current_branch,
            "is_protected": is_protected
        }
    )
```

**Continue bash commands:**

```bash

# Check for TypeScript errors (if tsconfig exists)
if [ -f "tsconfig.json" ]; then
  npx tsc --noEmit 2>&1 | tail -10
fi

# Check for package.json (Node project)
if [ -f "package.json" ]; then
  echo "Node project detected"
fi

# Check for TECHNICAL_DEBT.md
if [ -f "TECHNICAL_DEBT.md" ]; then
  head -50 TECHNICAL_DEBT.md
fi

# Check for open GitHub issues
gh issue list --limit 5 2>/dev/null || echo "No gh CLI or not a repo"
```

**RECORDING: After running bash commands above, record context files:**

```python
from popkit_shared.utils.session_recorder import is_recording_enabled, record_file_read
from pathlib import Path

if is_recording_enabled():
    # Record STATUS.json if it exists
    status_file = Path.cwd() / ".claude" / "STATUS.json"
    if status_file.exists():
        record_file_read(
            str(status_file),
            "Previous session context loaded",
            relevant=True
        )

    # Record TECHNICAL_DEBT.md if it exists
    tech_debt_file = Path.cwd() / "TECHNICAL_DEBT.md"
    if tech_debt_file.exists():
        record_file_read(
            str(tech_debt_file),
            "Technical debt items reviewed",
            relevant=True
        )
```

### Step 1.5: Detect Research Branches (NEW - Issue #181)

Check for research branches from Claude Code Web sessions:

```python
import sys
from popkit_shared.utils.research_branch_detector import (
    get_research_branches,
    format_branch_table
)
# RECORDING: Import session recording utilities
from popkit_shared.utils.session_recorder import (
    is_recording_enabled,
    record_reasoning,
    record_file_read
)

# Detect research branches
branches = get_research_branches()

# RECORDING: Log research branch detection
if is_recording_enabled():
    record_reasoning(
        step="Detect research branches",
        reasoning=f"Scanning remote branches for research content from web sessions",
        data={"branches_found": len(branches)}
    )

if branches:
    print("## Research Branches Detected\n")
    print(format_branch_table(branches))
    print("\nThese branches contain research from Claude Code Web sessions.")
    print("Use `pop-research-merge` skill to process them.")
```

**Research Branch Patterns:**

- `origin/claude/research-*` - Explicit research branches
- `origin/claude/*-research-*` - Topic-specific research
- Branches with `docs/research/*.md` or `RESEARCH*.md` files

### Step 2: Detect Project Context

Identify what kind of project and what state it's in:

| Indicator               | What It Means                   | Weight       |
| ----------------------- | ------------------------------- | ------------ |
| **On protected branch** | **Requires feature branch**     | **CRITICAL** |
| Uncommitted changes     | Active work in progress         | HIGH         |
| Ahead of remote         | Ready to push/PR                | MEDIUM       |
| TypeScript errors       | Build broken                    | HIGH         |
| **Research branches**   | Web session findings to process | HIGH         |
| Open issues             | Known work items                | MEDIUM       |
| **Issue votes**         | Community priority              | MEDIUM       |
| TECHNICAL_DEBT.md       | Documented debt                 | MEDIUM       |
| Recent commits          | Active development              | LOW          |

### Step 2.5: Fetch Issue Votes (NEW)

If GitHub issues exist, fetch community votes to prioritize:

```python
from popkit_shared.utils.priority_scorer import get_priority_scorer, fetch_open_issues
from popkit_shared.utils.session_recorder import is_recording_enabled, record_reasoning

# Fetch and rank issues by combined priority score
scorer = get_priority_scorer()
issues = fetch_open_issues(limit=10)
ranked = scorer.rank_issues(issues)

# RECORDING: Log issue prioritization
if is_recording_enabled():
    record_reasoning(
        step="Prioritize GitHub issues",
        reasoning=f"Fetched {len(issues)} issues, ranked by votes + staleness + labels",
        data={
            "total_issues": len(issues),
            "top_3_scores": [i.priority_score for i in ranked[:3]]
        }
    )

# Top-voted issues get recommendation priority
for issue in ranked[:3]:
    # issue.priority_score combines votes, staleness, labels, epic status
    print(f"#{issue.number} {issue.title} - Score: {issue.priority_score}")
```

**Vote Weights:**

- 👍 (+1) = 1 point (community interest)
- ❤️ (heart) = 2 points (strong support)
- 🚀 (rocket) = 3 points (approved/prioritized)
- 👎 (-1) = -1 point (deprioritize)

### Step 3: Score Recommendations

For each potential recommendation, calculate a relevance score:

```
Score = Base Priority + Context Multipliers

Base Priorities:
- Create feature branch (if on protected): 100  # NEW - HIGHEST PRIORITY
- Fix build errors: 90
- Process research branches: 85  # NEW - important to merge findings
- Commit uncommitted work: 80
- Push ahead commits (if on feature branch): 60  # UPDATED - only if safe
- Address open issues: 50
- Tackle tech debt: 40
- Start new feature: 30

Context Multipliers:
- On protected branch with commits: +50 to branch creation  # NEW
- Has uncommitted changes: +20 to commit
- TypeScript errors: +30 to fix
- Research branches detected: +25 to process
- Many open issues: +10 to issue work
- Long time since commit: +15 to commit
```

### Step 4: Generate Recommendations

Create 3-5 prioritized recommendations based on scores.

For each recommendation, provide:

1. **Command** - The exact popkit command to run
2. **Why** - Context-specific reason (not generic)
3. **What it does** - Brief description
4. **Benefit** - What user gains

## Output Format

Use the `next-action-report` output style:

```markdown
## Current State

| Indicator      | Status         | Urgency           |
| -------------- | -------------- | ----------------- |
| Current Branch | [branch-name]  | [urgency]         |
| Uncommitted    | X files        | [HIGH/MEDIUM/LOW] |
| Branch Sync    | [status]       | [urgency]         |
| TypeScript     | [clean/errors] | [urgency]         |
| Open Issues    | X open         | [urgency]         |

**Note:** When on protected branch (main/master), display urgency as:
```

| Current Branch | main (PROTECTED) | ⚠️ CRITICAL |

```

## Recommended Actions

### 1. [Primary Action] (Score: XX)

**Command:** `/popkit:[command]`
**Why:** [Specific reason based on detected state]
**What it does:** [Brief description]
**Benefit:** [What you gain]

### 2. [Secondary Action] (Score: XX)

...

### 3. [Tertiary Action] (Score: XX)

...

## Quick Reference

| If you want to...  | Use this command          |
| ------------------ | ------------------------- |
| Commit changes     | `/popkit:git commit`      |
| Review code        | `/popkit:git review`      |
| Get project health | `/popkit:routine morning` |
| Plan a feature     | `/popkit:dev brainstorm`  |
| Debug an issue     | `/popkit:debug`           |

## Alternative Paths

Based on your context, you could also:

- [Alternative 1]
- [Alternative 2]
```

## Recommendation Logic

### If On Protected Branch with Unpushed Commits (NEW - Issue #141)

````markdown
### 1. Create Feature Branch

**Command:** `git checkout -b feat/descriptive-name`

**Why:** You have [X] commits on `main` but cannot push directly due to branch protection

**What it does:**

- Creates feature branch from current state
- Moves all commits to feature branch
- Resets local main to match remote

**Benefit:**

- Complies with branch protection policy
- Enables proper PR workflow
- Prevents failed push attempts

**Next steps:**

```bash
# Create and push feature branch
git checkout -b feat/your-feature-name
git push -u origin feat/your-feature-name

# Create pull request
gh pr create --title "..." --body "..."

# Clean up local main
git checkout main
git reset --hard origin/main
```
````

````

**CRITICAL**: This recommendation should **suppress** the "Push ahead commits" recommendation when on a protected branch.

### If Uncommitted Changes Detected

```markdown
### 1. Commit Your Current Work

**Command:** `/popkit:commit`
**Why:** You have [X] uncommitted files including [key files]
**What it does:** Auto-generates commit message matching repo style
**Benefit:** Clean working directory, changes safely versioned
````

### If TypeScript Errors

```markdown
### 1. Fix Build Errors

**Command:** `/popkit:debug`
**Why:** TypeScript has [X] errors blocking build
**What it does:** Systematic debugging with root cause analysis
**Benefit:** Unblocked development, passing CI
```

### If Research Branches Detected (NEW - Issue #181)

```markdown
### 1. Process Research Branches

**Command:** Invoke `pop-research-merge` skill
**Why:** Found [X] research branch(es) from Claude Code Web sessions
**Branches:**
| Branch | Topic | Created |
|--------|-------|---------|
| `research-claude-code-features` | Claude Code Integration | 2h ago |

**What it does:** Merges research content, organizes docs, creates GitHub issues
**Benefit:** Research findings become actionable issues in your backlog
```

When research branches are detected, prompt the user:

```
Use AskUserQuestion tool with:
- question: "Found [X] research branch(es) from web sessions. Process them now?"
- header: "Research"
- options:
  - label: "Yes, process"
    description: "Merge findings and create issues (recommended)"
  - label: "Review first"
    description: "Show me what's in the branches"
  - label: "Skip for now"
    description: "Continue to other recommendations"
- multiSelect: false
```

If user selects "Yes, process" or "Review first", invoke the `pop-research-merge` skill.

### If Open Issues Exist

```markdown
### 2. Work on Open Issue

**Command:** `/popkit:dev work #[number]`
**Why:** Issue #[X] "[title]" is high priority (Score: XX)
**Votes:** 👍5 ❤️2 🚀1
**What it does:** Issue-driven development workflow
**Benefit:** Structured progress on community-prioritized work
```

When multiple issues exist, use priority scoring to recommend the best one:

```python
from popkit_shared.utils.priority_scorer import get_priority_scorer
from popkit_shared.utils.session_recorder import is_recording_enabled, record_recommendation

scorer = get_priority_scorer()
ranked = scorer.rank_issues(issues)

# Recommend highest-scored issue
top = ranked[0]
print(f"Work on #{top.number} '{top.title}' (Score: {top.priority_score:.1f})")
if top.vote_breakdown:
    print(f"Community votes: {scorer.vote_fetcher.format_vote_display(top, compact=True)}")

# RECORDING: Log the recommendation
if is_recording_enabled():
    record_recommendation(
        recommendation_type="issue",
        command=f"/popkit:dev work #{top.number}",
        priority_score=int(top.priority_score),
        reason=f"Issue #{top.number} '{top.title}' has highest community priority (votes + staleness + labels)"
    )
```

### If No Urgent Items

```markdown
### 1. Check Project Health

**Command:** `/popkit:routine morning`
**Why:** No urgent items - good time for health check
**What it does:** Comprehensive project status with "Ready to Code" score
**Benefit:** Identify hidden issues before they become urgent
```

## Quick Mode

When called with `quick` argument, provide condensed output:

```markdown
## /popkit:next (quick)

**State:** 5 uncommitted | branch synced | TS clean | 3 issues

**Top 3:**

1. `/popkit:git commit` - Commit 5 files (HIGH)
2. `/popkit:dev work #42` - Work on "Add auth" (MEDIUM)
3. `/popkit:routine morning` - Health check (LOW)
```

## Error Handling

| Situation            | Response                                |
| -------------------- | --------------------------------------- |
| Not a git repo       | Note it, skip git-based recommendations |
| No package.json      | Skip Node-specific checks               |
| gh CLI not available | Skip issue recommendations              |
| Empty project        | Recommend `/popkit:project init`        |

## Visual Style

Use components from `output-styles/visual-components.md`:

- Status indicators: ✓ (success), ✗ (failure), → (in progress)
- Urgency levels: HIGH (red), MEDIUM (yellow), LOW (blue), OK (green)
- Tables with status columns
- Quick reference tables

## Related

- `/popkit:next` command - User-facing wrapper
- `/popkit:routine morning` - Detailed health check
- `/popkit:dev brainstorm` - For when direction is truly unclear
- `pop-research-merge` skill - Process detected research branches
- `output-styles/next-action-report.md` - Full output template
- `output-styles/visual-components.md` - Reusable visual elements
- `user-prompt-submit.py` - Uncertainty trigger patterns
- `hooks/utils/vote_fetcher.py` - GitHub reaction fetching
- `hooks/utils/priority_scorer.py` - Combined priority calculation
- `hooks/utils/research_branch_detector.py` - Research branch detection
