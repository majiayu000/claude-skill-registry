---
name: lessons-capture
description: Use when concluding significant work to extract reusable patterns and anti-patterns
---

# Lessons Capture

## Overview

Distills session experiences into transferable, project-scoped knowledge.

**Core principle:** Extract patterns that will help future sessions on this project.

**Announce at start:** "Applying lessons-capture skill to extract reusable patterns."

## When to Use

- After completing a significant feature or bugfix
- When a pattern emerges that should be reused
- When discovering an anti-pattern to avoid
- When resolving a discrepancy (updating stale lesson)

> [!IMPORTANT]
> Lessons persist in the **PROJECT** (`<workspace>/.ai-memory/lessons/`), not the conversation.

## The Process

### Step 1: Identify Lesson-Worthy Patterns

Ask:
- Did I solve a problem that will recur?
- Did I discover a project-specific constraint?
- Did I find an anti-pattern to avoid?

### Step 2: Check for Existing Lessons

1. List `<workspace>/.ai-memory/lessons/`
2. If similar lesson exists: Update it with `supersedes` field
3. If new: Create fresh lesson

### Step 3: Write the Lesson

Create `<workspace>/.ai-memory/lessons/<slug>.md`:

```markdown
# Lesson: [Descriptive Title]

**Context**: [When this applies]
**Discovered**: YYYY-MM-DD
**Last Validated**: YYYY-MM-DD

## Pattern
[What to do - the reusable approach]

## Anti-Pattern
[What NOT to do - common mistakes]

## Evidence
- [Link to code or walkthrough showing this in action]

## Supersedes
- [Previous lesson file if updating, or omit]
```

### Step 4: Verify Lesson Quality

- Is it general enough to apply to similar future work?
- Is it specific enough to be actionable?
- Does it include both pattern AND anti-pattern?

## Common Mistakes

- Writing lessons too specific to one case
- Forgetting to link to evidence
- Not including the anti-pattern section
- Creating duplicate lessons instead of updating existing
- Using vague language ("handle appropriately")

## Checklist

Before committing lesson:

- [ ] Has clear `Context` for when it applies
- [ ] Has concrete `Pattern` (what to do)
- [ ] Has concrete `Anti-Pattern` (what NOT to do)
- [ ] Links to evidence (code, walkthrough, PR)
- [ ] Checked for existing similar lessons
- [ ] `Last Validated` date is current
