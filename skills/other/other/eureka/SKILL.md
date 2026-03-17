---
name: eureka
description: 'Capture technical breakthroughs and transform them into actionable, reusable documentation. Use this skill when the user has achieved a significant technical insight, solved a hard problem, discovered a non-obvious solution, or wants to document a breakthrough moment. Also trigger when the user mentions "eureka", "breakthrough", "document this insight", "capture this discovery", or wants to turn a technical win into reusable knowledge.'
---

# Eureka

Capture technical breakthroughs and transform them into actionable, reusable knowledge assets while context is fresh.

## Process

### 1. Capture the Breakthrough

When invoked, immediately gather the essential details:

- **What was the problem?** The specific challenge or blocker faced.
- **What was the insight?** The key realization that unlocked the solution.
- **What changed?** Concrete before/after differences (metrics, behavior, code).
- **Is there a minimal working example?** Request one if not provided.

Ask clarifying questions if any of these are unclear, but act fast — capture while context is fresh.

### 2. Create the Breakthrough File

Create a structured markdown file at `breakthroughs/YYYY-MM-DD-[brief-name].md` using today's date and a concise kebab-case name derived from the breakthrough.

Use this template:

```markdown
# [Descriptive Title]

**Date**: YYYY-MM-DD
**Tags**: [relevant, searchable, tags]

## One-Line Summary

A single sentence capturing the core insight.

## The Problem

What was the challenge? What wasn't working? Include specific error messages, performance numbers, or behavioral descriptions.

## The Insight

The key realization or discovery. What made this non-obvious? Why did previous approaches fail?

## Implementation

Minimal working code demonstrating the solution:

\`\`\`[language]
# concrete code example
\`\`\`

## Impact

| Metric | Before | After |
|--------|--------|-------|
| [relevant metric] | [value] | [value] |

## Reusable Pattern

Abstract the specific solution into a general principle that can be applied elsewhere:

- **When you see**: [symptom or situation]
- **Consider**: [the general approach]
- **Because**: [why it works]

## Related Resources

- Links to relevant documentation, issues, or discussions
```

### 3. Update the Index

Update `breakthroughs/INDEX.md` with a new entry. If the index file does not exist, create it with this structure:

```markdown
# Breakthrough Index

| Date | Title | Tags | Link |
|------|-------|------|------|
| YYYY-MM-DD | [Title] | [tags] | [link to file] |
```

Append the new entry to the table, keeping entries in reverse chronological order (newest first).

### 4. Extract Reusable Patterns

After documenting, help the user identify:

- Is this pattern applicable to other parts of the codebase?
- Could this become a lint rule, test, or automated check?
- Should this be shared with the team?

## Key Principles

- **Act fast**: Capture insights while context is fresh — don't over-polish on first pass.
- **Be specific**: Include concrete metrics, error messages, and code. Vague breakthroughs are not reusable.
- **Think reusable**: Always extract the generalizable pattern from the specific solution.
- **Stay searchable**: Use consistent tags and clear titles so breakthroughs can be found later.

## Your Task

Document the breakthrough based on what the user describes:

1. If the description is clear, proceed directly to creating the breakthrough file
2. If details are missing, ask focused clarifying questions first
3. Create the file, update the index, and highlight the reusable pattern
