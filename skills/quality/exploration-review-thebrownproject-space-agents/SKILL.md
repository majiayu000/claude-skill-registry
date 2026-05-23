---
name: exploration-review
description: "Interactive code review through conversation. HOUSTON guides review, spawns specialized agents, and helps create Beads for issues found."
---

# /exploration-review - Interactive Code Review

Review code through conversation. This is collaborative analysis, not a report dump. You guide the review, ask questions, spawn specialized agents, and work through findings together.

## The Process

1. **Understand scope** - What code to review? Recent changes, specific files, or feature area?
2. **Ask which categories** - Quality, security, performance, simplification, or all?
3. **Spawn relevant agents** - Run in background while you talk
4. **Work through findings** - Discuss issues, get context, prioritize
5. **Create report** - Summarize findings by priority
6. **Offer Beads** - Ask if user wants to track issues

## Starting the Review

### 1. Determine Scope

Ask what to review:
- Recent changes (git diff)
- Specific files or directories
- A feature or component
- Code from last /mission

### 2. Select Categories

Use AskUserQuestion:
```
"Which areas should I focus on?"
Options:
- Quality (readability, structure, patterns)
- Security (secrets, injection, validation)
- Performance (algorithms, queries, optimization)
- Simplification (dead code, over-engineering, DRY)
- All of the above
```

### 3. Spawn Agents

Based on selection, spawn with `run_in_background: true`:

| Category | Agent | Focus |
|----------|-------|-------|
| Quality | `space-agents:review-quality` | Readability, naming, complexity, patterns |
| Security | `space-agents:review-security` | Secrets, injection, auth, OWASP |
| Performance | `space-agents:review-performance` | Algorithms, queries, caching, bundle |
| Simplification | `space-agents:review-code-simplifier` | Dead code, over-engineering, DRY, bloat |

Continue conversation while agents work. Check results with `TaskOutput block: false`.

## Working Through Findings

### Priority Levels

Categorize all findings:

| Priority | Meaning | Action |
|----------|---------|--------|
| **Critical** | Security vulnerability, data loss risk, broken functionality | Must fix before merge |
| **Warning** | Code smell, maintainability issue, potential bug | Should fix |
| **Suggestion** | Style improvement, optimization opportunity | Consider improving |

### Discussion Flow

For each finding:
1. **Present the issue** - What, where, why it matters
2. **Get context** - Ask if there's a reason for current approach
3. **Discuss fix** - Agree on solution or accept as-is
4. **Categorize** - Confirm priority level

**Red flags to watch for:**
- User dismissing Critical issues - push back
- "It works so it's fine" - explain long-term cost
- Over-engineering suggestions - keep it practical

## Your Role

- **Ask questions** - Understand context before judging
- **Have opinions** - Recommend priorities, push back on bad patterns
- **Suggest agents, don't auto-spawn** - Always ask first
- **Be constructive** - Acknowledge what's done well, not just problems
- **Keep talking** - Never wait silently for agent results

## Available Agents

Spawn with `run_in_background: true`, continue conversation immediately:

- `space-agents:review-quality` - Code quality and maintainability
- `space-agents:review-security` - Security vulnerabilities and risks
- `space-agents:review-performance` - Performance issues and optimizations
- `space-agents:review-code-simplifier` - Dead code, over-engineering, DRY violations

## AskUserQuestion (Required)

**Always use `AskUserQuestion`** for every question in review. Prefer multiple choice when you can anticipate likely answers.

## Output

When review is complete:

### 1. Summary Report

Present findings organized by priority:

```
## Review Summary

### Critical (must fix)
- [Issue with file:line reference]

### Warnings (should fix)
- [Issue with file:line reference]

### Suggestions (consider)
- [Issue with file:line reference]

### What's Good
- [Positive observations]
```

### 2. Offer Beads

Ask user:
```
AskUserQuestion:
  "Want to create Beads to track these issues?"
  Options:
  - "Yes, create bugs for Critical/Warning" - Track issues that need fixing
  - "Yes, create tasks for all" - Track everything including suggestions
  - "No, I'll handle it" - Skip Bead creation
```

**If creating Beads:**
- Use `bd create --type=bug` for Critical/Warning issues
- Use `bd create --type=task` for Suggestions
- Include file:line references in description
