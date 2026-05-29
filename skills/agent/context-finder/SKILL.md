---
name: context-finder
description: Auto-spawn context-finder agent for search tasks. Use when user says "find", "search", "where is", "look for", "trace", "what file", "which commit", "grep", "locate". Triggers search in git history, files, issues, retrospectives.
---

# Context Finder Skill

> Auto-trigger search when user needs to find something

## Proactive Triggers

### MUST Spawn context-finder Agent When:
- User says: "find", "search", "where is", "look for"
- User says: "what file", "which commit", "locate"
- User asks: "did we work on X", "when did we", "where did"
- User needs to trace: code, history, issues, docs

### How to Invoke

Spawn the context-finder agent:

```
Task tool:
  subagent_type: context-finder
  model: haiku
  prompt: |
    Search for [USER'S QUERY] in:
    1. Git history: git log --all --oneline --grep="[QUERY]"
    2. Files: find/grep for [QUERY]
    3. GitHub issues: gh issue list --search "[QUERY]"
    4. Retrospectives: grep in ψ/memory/retrospectives/

    Return: compact list of matches with paths/commits
```

## What context-finder Searches

| Source | Command | Finds |
|--------|---------|-------|
| Git history | `git log --grep` | Commits mentioning topic |
| Files | `find`, `grep` | Current files |
| Issues | `gh issue list` | Planning, discussions |
| Retrospectives | `grep ψ/memory/` | Past session context |

## When NOT to Use

- User already knows the exact file path
- Simple questions about current code (just read it)
- User explicitly says "don't search"

## Quick Patterns

| User Says | Action |
|-----------|--------|
| "find the auth code" | Spawn agent → search "auth" |
| "where did we put X" | Spawn agent → search files + git |
| "when did we work on Y" | Spawn agent → search retrospectives |
| "trace Z" | Spawn agent → comprehensive search |
