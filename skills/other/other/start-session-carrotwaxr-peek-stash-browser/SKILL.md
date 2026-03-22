---
name: start-session
description: Use when starting a new coding session, beginning work on a branch, or resuming after a context reset. Gathers branch context, in-progress work, plan documents, and recent history to produce a briefing before any code is written.
---

# Start Session

Orientation before action. Gather context from the current branch, git state, plan documents, and recent history, then present a structured briefing.

**Announce at start:** "Using start-session to orient before we begin."

## Step 1: Detect Current State

```bash
# Branch name
git branch --show-current

# Is this main or a feature branch?
# main/master = fresh start, anything else = in-progress work

# Uncommitted changes
git status --short

# Recent commits on this branch (diverged from main)
git log main..HEAD --oneline 2>/dev/null || git log --oneline -5
```

## Step 2: Identify Context Sources

Based on the branch name, find relevant context:

### Plan Documents

```bash
# Search for plan docs matching branch topic
ls docs/plans/ | grep -i "<branch-topic-keywords>"

# Also check for today's date or recent dates
ls docs/plans/ | tail -10
```

If a plan doc exists, read it and extract:
- Current status
- Implementation phases
- Key decisions made

### Related Issues

```bash
# Search GitHub issues related to branch topic
gh issue list --search "<branch-topic-keywords>" --state all --limit 5
```

### Recent Git Activity

```bash
# What was the last session working on?
git log --oneline -10 --format="%h %s (%ar)"

# Any stashed work?
git stash list
```

## Step 2b: Query the Brain

Search the MCP memory service for context relevant to the branch topic or planned work:

```
memory_search(query: "<branch-topic-keywords>", limit: 5)
memory_search(query: "gotchas <area>", limit: 5)
```

Look for:
- Prior decisions and their rationale
- Known gotchas in the area being worked on
- Patterns established in previous sessions
- Bug history and recurring issues

Include relevant brain findings in the briefing under a "Brain Context" section.

## Step 3: Check Project Health

Quick health check — catch problems before they compound:

```bash
# Are there uncommitted changes that might be from a crashed session?
git status --short

# Are we behind main?
git fetch origin main --quiet 2>/dev/null
git rev-list HEAD..origin/main --count 2>/dev/null
```

## Step 4: Present Briefing

Format the gathered information as a structured briefing:

```
## Session Briefing

**Branch**: `<branch-name>` (diverged from main by N commits)
**Status**: <fresh | in-progress | uncommitted changes detected>

### Context
- <Plan doc summary if found, or "No plan doc found">
- <Related issues if found>
- <Recent commit summary>

### Relevant Skills
Based on the branch topic, these skills are likely relevant:
- <skill-1>: <why>
- <skill-2>: <why>

### Suggested Next Steps
- <Based on branch state and plan doc status>
```

## Step 5: Confirm Direction

After presenting the briefing, ask:

> Does this look right? What are we working on today?

Wait for human confirmation before proceeding to any code changes. The briefing may be wrong or outdated — the human corrects course here.

## Branch Name Convention Decoding

Branch names encode intent:

| Prefix | Meaning | Expected workflow |
|--------|---------|-------------------|
| `feat/` | New feature | Plan → implement → test → PR |
| `fix/` | Bug fix | Investigate → fix → regression test → PR |
| `refactor/` | Code improvement | Understand scope → refactor → verify tests → PR |
| `docs/` | Documentation | Draft → review → PR |
| `chore/` | Maintenance | Execute → verify → PR |

## Skill Suggestions by Area

Map branch topics to relevant skills:

| Topic keywords | Skills to suggest |
|---------------|-------------------|
| video, proxy, stream, hls | `express5-api-patterns`, `stash` |
| sync, instance, multi | `express5-api-patterns`, `prisma-sqlite-expert` |
| ui, component, page, layout | `visual-style`, `react-spa-performance` |
| test, coverage, spec | `writing-tests`, `vitest` |
| release, version, deploy | `release-workflow` |
| restriction, exclusion, permission | `prisma-sqlite-expert`, `express5-api-patterns` |
| migration, schema, database | `prisma-sqlite-expert` |
| playlist, rating, stats | `express5-api-patterns`, `prisma-sqlite-expert` |
| graphql, codegen, stash-client | `graphql-patterns`, `stash` |

## What This Skill Does NOT Do

- Does not make decisions about what to work on (that's the human's call)
- Does not start coding (wait for confirmation)
- Does not replace `work-ticket` (which handles the full ticket lifecycle)
- Queries brain for context but does not store new memories (that happens at work completion)
