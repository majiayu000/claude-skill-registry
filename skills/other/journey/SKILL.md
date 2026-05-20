---
name: journey
updated: 2026-02-20
description: Create session learning logs that persist institutional memory across Claude Code sessions.
user-invocable: true
allowed-tools: Read, Write, Glob, Bash
---

# Journey Skill

Create or read session learning logs that persist institutional memory across Claude Code sessions.

## When to Use

Use `/journey` when:
- After completing significant work in a session
- After discovering important patterns or learnings
- After making architectural decisions
- After fixing non-trivial bugs
- When the session contains knowledge worth preserving

## Commands

### Create New Journey
```
/journey {title}
```
Creates a new journey file with a summary of the current session.

### List Journeys
```
/journey --list
```
Shows all existing journeys.

### Read Journey
```
/journey --read {filename}
```
Reads a specific journey file.

### Show Recent
```
/journey --recent
```
Shows the 5 most recent journeys.

## Journey File Format

Journeys are saved to `.claude/journeys/` with naming: `YYYY-MM-DD-{slug}.md`

### Template Structure

```markdown
# Journey: {Title}

**Date:** YYYY-MM-DD
**Tags:** #tag1 #tag2 #tag3

## Summary

1-3 sentences describing what was accomplished and why it matters.

## What Was Done

1. **First major item**
   - Details
   - More details

2. **Second major item**
   - Details

## Key Learnings

- **Learning 1**: Explanation with context
- **Learning 2**: Explanation with context

## Files Changed

| File | Change |
|------|--------|
| `path/to/file.ts` | Brief description |

## Patterns Discovered

### Pattern Name
\`\`\`code
// Example code showing the pattern
\`\`\`

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Choice made | Why it was made |

## Connected To

- Related skills, files, or future work
```

## Writing Guidelines

### Summary
- Be concise but specific
- Mention the "why" not just the "what"
- Future Claude sessions should understand the context

### Key Learnings
- Focus on insights that prevent future mistakes
- Include code patterns when relevant
- Explain the "gotcha" moments

### Tags
Common tags:
- `#bugfix` - Bug fixes
- `#feature` - New features
- `#refactor` - Code restructuring
- `#tooling` - Build/dev tooling
- `#performance` - Performance work
- `#meta` - Claude Code/skills work
- `#architecture` - Architectural decisions
- `#security` - Security-related work

## Purpose

Journeys create **institutional memory** that:
1. Helps future sessions avoid repeating mistakes
2. Documents decisions and their rationale
3. Preserves patterns and best practices
4. Tracks the evolution of the codebase

Unlike git commits (which track *what* changed), journeys track *why* and *what was learned*.
