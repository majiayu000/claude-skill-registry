---
name: farm-audit
description: Audit all Farmwork systems and update FARMHOUSE.md metrics. Use when user says "open the farm", "audit systems", "check farm status", "update farmhouse", "project health", or asks about the current state of the project.
allowed-tools: Bash(*), Task, Read, Edit, Glob, Grep
---

# Farm Audit Skill

Comprehensive audit of all Farmwork systems. Updates `_AUDIT/FARMHOUSE.md` with current metrics.

## When to Use
- User wants to check project health
- Starting a new work session
- Before major releases
- Periodic maintenance check

## Workflow

### Step 1: Launch the-farmer Agent
Spawn the `the-farmer` agent to gather all metrics.

### Step 2: Gather Metrics
1. Count commands: `ls -1 .claude/commands/*.md 2>/dev/null | wc -l`
2. Count agents: `ls -1 .claude/agents/*.md 2>/dev/null | wc -l`
3. Count skills: `ls -d .claude/skills/*/ 2>/dev/null | wc -l`
4. Count tests: `find . -name "*.test.*" -not -path "./node_modules/*" | wc -l`
5. Count completed issues: `bd list --status closed 2>/dev/null | wc -l`

### Step 3: Tend the Idea Garden
Read `_AUDIT/GARDEN.md` and check idea ages:
- **Fresh** (0-44 days): No action needed
- **Wilting** (45-60 days): Mark with ⚠️ in output
- **Composted** (60+ days): Move to `_AUDIT/COMPOST.md`

### Step 4: Check Research Freshness
Read `_RESEARCH/*.md` files and check ages:
- **Fresh** (0-14 days): Current and reliable
- **Aging** (15-30 days): Consider refreshing
- **Stale** (30+ days): Recommend update

### Step 5: Update FARMHOUSE.md
Update `_AUDIT/FARMHOUSE.md` with:
- Current date
- All metrics
- Score based on completeness
- Audit history entry

## Output Format
```
## Farm Audit Complete

### Metrics
- Commands: X
- Agents: X
- Skills: X
- Tests: X files
- Completed Issues: X

### Idea Garden
- Active: X ideas
- Wilting: X ideas (list if any)
- Auto-composted: X ideas

### Research Library
- Fresh: X docs
- Aging: X docs
- Stale: X docs

### Score: X/10
```
