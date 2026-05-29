---
name: bootstrap
description: This skill should be used when the user asks to "create a bootstrap prompt", "handoff", "save session state", "continue in new session", "create handoff", "session summary for continuation", "bootstrap for fresh session", or wants to capture the current session state for resumption in a new Claude Code session.
---

# Bootstrap Prompt Generator

Generate a detailed context prompt that enables seamless continuation of work in a fresh Claude Code session.

## Purpose

Sessions accumulate valuable context: task understanding, decisions made, patterns discovered, gotchas encountered, and progress achieved. When starting fresh, this knowledge is lost. A bootstrap prompt preserves the essential context needed to continue effectively.

## Core Principle: Intelligent Context Selection

Do NOT mechanically dump everything. Analyze what actually matters for continuation:

- **What would confuse a fresh Claude?** Include it.
- **What decisions took deliberation?** Document the reasoning.
- **What gotchas caused wasted time?** Warn about them.
- **What's the critical path forward?** Clarify it.

Omit: routine operations, obvious context, resolved dead-ends, standard patterns.

## Analysis Process

### 1. Assess Session Significance

Determine what kind of work occurred:
- **Exploration**: Learning codebase, investigating options
- **Implementation**: Building features, fixing bugs
- **Debugging**: Tracking down issues, testing hypotheses
- **Planning**: Designing architecture, making decisions

Each type has different handoff needs.

### 2. Identify Essential Context

**Project State**
- Working directory and project identity
- Tech stack if non-obvious
- Branch and git state (use `scripts/gather-git-state.sh`)

**Task Context**
- Original objective (what the user asked for)
- Current interpretation (what we understood it to mean)
- Scope decisions (what's in/out)

**Progress Assessment**
- What's completed and working
- What's in progress and current state
- What's remaining (check todo list)
- What's blocked and why

**Critical Knowledge**
- Architectural decisions and their rationale
- Patterns established in this session
- Gotchas and workarounds discovered
- Files that are central to the work

**Next Actions**
- Immediate next step
- Remaining work outline
- Known unknowns to investigate

### 3. Determine Depth

Scale detail to session complexity:

**Light session** (quick task, simple fix): Brief summary, next step
**Medium session** (feature work, debugging): Key decisions, progress, gotchas
**Deep session** (architecture, complex debug): Full context with reasoning

## Output Format

Generate a markdown document structured as a prompt for a fresh session:

```markdown
# Bootstrap: [Brief Task Description]

> Generated: [timestamp]
> Project: [project path]
> Branch: [branch name]

## Context

[2-4 sentences on what this project/task is about]

## Session Summary

[What happened in the session - decisions, progress, discoveries]

## Current State

[Where things stand right now - what works, what's in progress]

## Key Files

[List of files central to the work with brief descriptions]

## Decisions Made

[Important choices with brief rationale - only if non-obvious]

## Gotchas & Warnings

[Things that caused problems or need careful handling]

## Next Steps

[Prioritized list of what to do next]

## Resume Instructions

[Specific guidance on how to continue - commands to run, files to open, etc.]
```

Omit sections that aren't relevant. A simple task might only need Context, Current State, and Next Steps.

## Execution Steps

1. **Analyze the session** - Review conversation, understand what happened
2. **Run git state script** - Execute `scripts/gather-git-state.sh` to capture repository state
3. **Check todo list** - Review current todos for progress context
4. **Identify key files** - Determine which files are central to the work
5. **Draft bootstrap prompt** - Write the document following the format above
6. **Determine output path** - Use `.claude/handoffs/{project-name}-{YYYYMMDD-HHMMSS}.md`
7. **Save the file** - Write the bootstrap prompt to the handoffs directory
8. **Copy to clipboard** - Execute `scripts/copy-to-clipboard.sh {filepath}` to copy contents

## File Locations

- **Output directory**: `.claude/handoffs/` (create if doesn't exist)
- **Filename pattern**: `{project-name}-{YYYYMMDD-HHMMSS}.md`
- **Project name**: Derive from git remote, directory name, or package.json

## Scripts

### `scripts/gather-git-state.sh`

Collects repository state: branch, recent commits, uncommitted changes, modified files.
Run this first to include accurate git context in the bootstrap prompt.

### `scripts/copy-to-clipboard.sh`

Copies file contents to system clipboard (macOS `pbcopy`).
Run after saving the bootstrap prompt file.

## Quality Checklist

Before finalizing, verify:

- [ ] Fresh Claude could understand the task without prior context
- [ ] Decisions include enough rationale to avoid re-litigating
- [ ] Gotchas are specific enough to be actionable
- [ ] Next steps are concrete and prioritized
- [ ] No unnecessary detail that obscures the important parts

## Example Bootstrap Prompts

### Light Session Example

```markdown
# Bootstrap: Fix API rate limiting bug

> Generated: 2025-01-15 14:30
> Project: /Users/dev/acme-api
> Branch: fix/rate-limiter

## Context

Fixing a bug where rate limiting wasn't being applied to the `/search` endpoint.

## Current State

Found the issue - the rate limiter middleware was added after the route registration.
Fix is ready but untested.

## Next Steps

1. Run test suite: `npm test`
2. If passing, commit with message "Fix rate limiter middleware order for /search"
```

### Deep Session Example

See `references/deep-session-example.md` for a complex multi-day project handoff.
