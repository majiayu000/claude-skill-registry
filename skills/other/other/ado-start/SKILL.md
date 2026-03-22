---
name: ado-start
description: Use when starting work on an Azure DevOps ticket. Triggers on "start ticket", "work on ticket", ticket number with implementation intent, or requests to plan a feature from a ticket.
model: sonnet
---

# Start Ticket

Fetch Azure DevOps ticket, resolve repo, create branch, explore codebase, create implementation plan.

> **Read `~/.claude/skills/_ado-shared.md`** for auth, env vars, fetch/update ticket patterns, and Windows/MSYS2 notes.

## Workflow

1. **Fetch ticket** via ADO REST API (see shared)
2. **Resolve repo** from `Custom.Repository` field (see below)
3. **Find upstream remote** in the resolved repo (see below)
4. **Create branch**: `git fetch <upstream> master && git checkout -b <ticketnr>-<short-desc> <upstream>/master`
5. **Update ticket state** to "In Progress" via REST API (see shared)
6. **Explore codebase** using Task tool with Explore subagent
7. **Ask clarifying questions** about implementation approach
8. **Enter plan mode** and write implementation plan

## Repo Resolution

The `Custom.Repository` field contains the GitHub repo name (semicolon-separated if multiple).

1. Read `Custom.Repository` from fetched work item fields
2. If present: take first value (before `;`), find matching directory in `/c/dev/` (local dir name matches repo name)
3. If absent: fall back to `ado-investigate` skill
4. `cd` into the resolved repo directory before continuing

## Upstream Remote Detection

Remote names vary. Detect dynamically:

```bash
git remote -v | grep 'bluebillywig/' | grep fetch | head -1 | awk '{print $1}'
```

If none found, list remotes and ask user.

## Branch Naming

Format: `<ticketnr>-<short-description>` (kebab-case, max 4-5 words from title)

Examples: `17858-shorts-shelf-autoplay`, `17432-devicePixelRatio-thumbs`

## CRITICAL: Ticket Number in Branch + PR Title

**Always** include the ADO ticket number in:
1. **Branch name**: `<ticketnr>-<short-desc>`
2. **PR title**: ` #<ticketnr>` suffix — e.g. `Show metadata toggle #18014`

## Exploration Strategy

Use Task tool with `subagent_type: Explore` to understand:
- Relevant components and their location
- Existing patterns and conventions
- Related props/configuration options
- How similar features are implemented

## Plan Structure

```markdown
# Plan: <ticketnr> - <short title>

## Context
<1-2 sentences from ticket description>

## Implementation
1. <Step with file path and specific change>
2. <Step with file path and specific change>

## Files to Modify
- <file path> - <what changes>

## Verification
1. <How to test the changes>
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Hardcoding remote name | Detect upstream remote dynamically via `git remote -v` |
| Wrong base branch | Always fetch + branch from `<upstream>/master`, not `main` or local master |
| Starting code before plan | Explore -> clarify -> plan -> implement |
| Not cd'ing to repo | Must cd into resolved repo before git/explore operations |
| Missing API research | Check related repos for API endpoints if needed |
