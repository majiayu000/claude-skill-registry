---
name: sanity-check
description: "Step back, reflect on current work, validate direction and alignment. Use when complexity is increasing, feeling uncertain, before major decisions, or something feels off."
model: claude-opus-4-5-20251101
allowed-tools: Read, Glob, Grep
---

# /sanity-check

Mid-work validation using reflection to catch drift early. Permission to pause and think.

## Usage

```bash
/sanity-check                        # Reflect on current work
/sanity-check --project coordinatr   # Focus on specific project
```

## When to Use

- Complexity is increasing
- Feeling uncertain about direction
- Before major decisions
- Something feels off
- After 30+ minutes of planning work

**Not for**: Session start (use /refresh), after completion (just continue)

## Execution Steps

### 1. Reflect Using Sequential Thinking

Process these questions:
- What are we trying to accomplish?
- What have we done so far?
- What's the current approach?
- Does this align with the project vision?
- Are we solving the right problem?
- What concerns exist?

**Categorize findings:**
- Green: On track, continue
- Yellow: Minor issues, easy fixes
- Red: Major drift, course correction needed

### 2. Read Context Files

```bash
# Project context (if specified)
Read: ideas/{project}/README.md
Read: ideas/{project}/project-brief.md
Read: ideas/{project}/critique.md

# General context
Read: CLAUDE.md
Read: about-me.md

# Recent work
Bash: git log -5 --format="%h - %s"
```

Skip missing files gracefully.

### 3. Analyze Alignment

Check against:
- **Vision**: Does current work support project goals?
- **Brief**: Are we addressing the stated problem?
- **Critique**: Are we avoiding known pitfalls?
- **Patterns**: Are we following repo conventions?

### 4. Provide Assessment

```markdown
## Sanity Check

### Current State
[What we're working on, current approach]

### Alignment Check
- **Vision**: [status] [brief assessment]
- **Problem Fit**: [status] [brief assessment]
- **Approach**: [status] [brief assessment]

### Concerns

**What's Working**
- [Positive observation]

**Minor Issues**
- [Yellow flag + suggested fix]

**Critical Issues**
- [Red flag + required action]

### Recommendation
[Continue as-is | Minor adjustment | Course correction | Pause and discuss]

### Next Steps
1. [Specific action]
2. [Specific action]
```

## Philosophy

- **Permission to pause**: Makes stepping back a legitimate workflow step
- **Catch drift early**: Course correction cheap now, expensive later
- **Trust your gut**: If something feels off, run this command
