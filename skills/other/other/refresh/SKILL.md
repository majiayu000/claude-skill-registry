---
name: refresh
description: "Silently refresh AI context by reading project configuration and guidelines. Use when starting a new conversation, after context loss, or before major tasks."
model: claude-haiku-4-5-20251001
allowed-tools: Read, Glob, Bash(date:*, ls:*)
---

# /refresh

Silently reload project context by reading critical configuration files.

## Usage

```bash
/refresh    # Silent context reload
```

## Execution Steps

### 1. Read Core Configuration

```bash
Read: CLAUDE.md
Read: .claude/memories/about-taylor.md
```

**Error if CLAUDE.md missing**: "CLAUDE.md not found"

### 2. Read Recent Memories

Get today's date and read memories from the last 3 days:

```bash
Bash: date +%Y-%m-%d  # Get today's date
Bash: ls .claude/memories/2026-01-*.json | tail -10  # Recent memory files
```

Read any memory files from the last 3 days (by filename date prefix).

### 3. Read Shared Documentation

```bash
Glob: shared/docs/**/*.md
# Read each found file
```

Skip silently if not found.

### 4. Get Recent Activity

```bash
Bash: git log -3 --format="%h - %s"
```

Skip if git unavailable.

### 5. Output

```
Context refreshed
```

**Silent operation**: Do NOT summarize files, list what was read, or explain context.

## What Gets Loaded

| Category | Files |
|----------|-------|
| Core | CLAUDE.md |
| Profile | .claude/memories/about-taylor.md |
| Memories | .claude/memories/YYYY-MM-DD-*.json (last 3 days) |
| Shared | shared/docs/**/*.md |
| Git | Last 3 commits |

## Error Handling

| Situation | Action |
|-----------|--------|
| CLAUDE.md missing | Error message |
| Other files missing | Skip silently |
| Git unavailable | Skip git, continue |

## When to Use

- Starting a new conversation
- After long break in session
- Before major planning work
- When context feels stale

**Not for**: Mid-task validation (use /sanity-check), project-specific context (read files directly)
