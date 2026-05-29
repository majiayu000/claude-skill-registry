---
name: milestone-tracker
description: Track GitHub milestone progress and issue completion. Use when user asks about milestone status, how many issues done, sprint progress, or completion percentage.
allowed-tools: Bash, Read
---

# Milestone Tracker Skill

## Purpose

Fetch and summarize milestone progress when the user asks about completion status, remaining work, or sprint metrics. This is a read-only skill.

## When to Use This

- User asks "milestone progress?"
- User asks "how many issues left?"
- User asks "completion percentage"
- User asks "what's left in the sprint?"
- User mentions milestone tracking

## Commands

### List All Milestones

```bash
gh api repos/joeczar/code-graph-mcp/milestones --jq '.[] | {number, title, open_issues, closed_issues, due_on, state}'
```

### Get Specific Milestone

```bash
gh api repos/joeczar/code-graph-mcp/milestones/<number>
```

### Get Issues in Milestone

```bash
gh issue list --milestone "<milestone-name>" --state all --json number,title,state,labels
```

### Calculate Progress

```
Completion % = (closed_issues / (open_issues + closed_issues)) * 100
```

## Current Milestones

| Milestone | Focus | Issues |
|-----------|-------|--------|
| M2: MCP Server Foundation | Server scaffold, basic tools | 7 |
| M3: Code Graph | Parse code, queries, MCP tools | 16 |
| M4: Documentation | Extract & link docs | 8 |
| M5: Knowledge Graph | Learnings, LLM extraction | 10 |
| M6: Semantic Search | Embeddings, hybrid search | 7 |
| M7: Workflow Checkpoint | Workflow state, resume | 6 |
| M8: Session Hooks & CLI | CLI, warmup/capture | 8 |

## Output Format

```markdown
## Milestone: <name>

**Progress:** X/Y issues (Z%)
**Due:** <date or "No due date">

### Progress Bar
[████████░░░░░░░░░░░░] 40% (8/20)

### By Status
- Done: <count>
- In Progress: <count>
- Not Started: <count>

### Recently Completed
- #X: <title>
- #Y: <title>

### Up Next (Open)
- #A: <title>
- #B: <title>
```

## Progress Bar Generation

Generate visual progress:

```bash
# Calculate percentage
OPEN=$(gh api repos/joeczar/code-graph-mcp/milestones/<n> --jq '.open_issues')
CLOSED=$(gh api repos/joeczar/code-graph-mcp/milestones/<n> --jq '.closed_issues')
TOTAL=$((OPEN + CLOSED))
PCT=$((CLOSED * 100 / TOTAL))

# Generate bar (20 chars)
FILLED=$((PCT / 5))
EMPTY=$((20 - FILLED))
BAR=$(printf '█%.0s' $(seq 1 $FILLED))$(printf '░%.0s' $(seq 1 $EMPTY))
echo "[$BAR] $PCT% ($CLOSED/$TOTAL)"
```

## Full Status Report

```bash
# Get all milestones with progress
gh api repos/joeczar/code-graph-mcp/milestones --jq '.[] | "\(.title): \(.closed_issues)/\(.open_issues + .closed_issues) (\(.closed_issues * 100 / ((.open_issues + .closed_issues) | if . == 0 then 1 else . end))%)"'
```
