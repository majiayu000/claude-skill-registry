---
name: rem-sleep
description: Memory consolidation and defragmentation for long-term memory maintenance. Use when asked to consolidate memories, defrag memory, run REM sleep, clean up memory files, or process session logs into durable memory. Also use periodically during heartbeats for memory maintenance.
homepage: https://github.com/stewnight/rem-sleep-skill
---

# REM Sleep - Memory Consolidation for AI Agents

Like biological REM sleep, this skill processes raw experience (session logs) into consolidated long-term memory.

**Works with:** OpenClaw, Claude Code, or any agent with session logs and memory files.

## The Problem

- Session logs accumulate but are expensive to re-read
- Important insights get buried in noise
- "Mental notes" don't survive context compaction
- After a restart, you're starting from scratch unless you wrote it down

## The Solution

Periodic "sleep cycles" that:
1. Search session logs for significant patterns
2. Extract what's worth remembering
3. Consolidate into durable memory files

## Modes

### 1. Consolidate
Process recent session logs → extract significant events → update MEMORY.md

### 2. Defrag
Review MEMORY.md → remove stale/outdated entries → merge duplicates → compress

### 3. Full
Run both consolidate then defrag.

---

## Consolidation Workflow

### Step 1: Gather Recent Sessions

**Option A: Using grep/jq (no extra software)**

```bash
# OpenClaw session logs location
SESSIONS_DIR="$HOME/.openclaw/agents/main/sessions"

# Search for patterns in recent sessions
grep -r "decision\|learned\|important\|remember\|TODO" "$SESSIONS_DIR" --include="*.jsonl" | head -100

# Parse JSONL and search content
find "$SESSIONS_DIR" -name "*.jsonl" -mtime -3 -exec cat {} \; | \
  jq -r 'select(.content) | .content' 2>/dev/null | \
  grep -i "decision\|learned\|important"
```

**Option B: Using Repo Prompt (if installed)**

```bash
# More powerful semantic search
rp -e 'search "decision" --context-lines 2'
rp -e 'search "learned" --context-lines 2'
rp -e 'search "important" --context-lines 2'
```

**Option C: Using memory_search (OpenClaw built-in)**

If your agent has the `memory_search` tool, use it to semantically search memory files:
```
memory_search("decisions made this week")
memory_search("lessons learned")
```

### Step 2: Identify Consolidation Candidates

From search results, look for:
- **Decisions made** — choices, preferences, conclusions
- **Facts learned** — new info about people, projects, systems
- **Lessons** — things that worked/didn't, mistakes to avoid
- **TODOs/commitments** — things promised or planned
- **Relationship context** — interactions with people, their preferences

### Step 3: Update Memory Files

**Two-tier system:**

1. **Daily file** (`memory/YYYY-MM-DD.md`): Raw events, specific details
2. **MEMORY.md**: Distilled, durable knowledge worth keeping long-term

**Consolidation prompt:**
> Review these session excerpts. Extract significant information that should be remembered long-term. Focus on: decisions, facts about people/projects, lessons learned, and preferences. Format as bullet points suitable for MEMORY.md.

---

## Defrag Workflow

### Step 1: Analyze Current Memory

Read MEMORY.md and identify:
- **Stale entries** — outdated info, completed TODOs, old dates
- **Duplicates** — same info repeated in different sections
- **Inconsistencies** — conflicting information
- **Bloat** — overly verbose entries that could be compressed

### Step 2: Categorize Issues

```
STALE: [entry] — reason it's outdated
DUPLICATE: [entry A] ≈ [entry B]
INCONSISTENT: [entry A] vs [entry B]
BLOAT: [verbose entry] → [compressed version]
```

### Step 3: Apply Fixes

- Remove stale entries (or move to an archive section if uncertain)
- Merge duplicates into single authoritative entry
- Resolve inconsistencies (check session logs if needed)
- Compress verbose entries

### Step 4: Reorganize

Ensure MEMORY.md has logical sections:
- About [User]
- My Setup
- Projects
- People
- Preferences
- Lessons Learned

---

## Scheduling

**Recommended cadence:**
- **Consolidate**: Every few days, or after busy periods
- **Defrag**: Weekly or bi-weekly
- **Full**: Monthly deep clean

**Trigger options:**
- Manually: "Run REM sleep" / "Consolidate my memories"
- Heartbeat: Add to HEARTBEAT.md for periodic runs
- Cron: Schedule isolated job for off-hours

---

## Quick Reference

```bash
# Native search (no dependencies)
grep -r "pattern" ~/.openclaw/agents/main/sessions --include="*.jsonl"

# With Repo Prompt
rp -e 'search "PATTERN" --context-lines 2'

# Helper script (if using Repo Prompt)
./scripts/gather-sessions.sh [days_back]
```

## File Structure

```
rem-sleep/
├── SKILL.md          # This file
├── README.md         # GitHub readme
└── scripts/
    └── gather-sessions.sh   # Helper script (requires Repo Prompt)
```

## Notes

- Session logs are JSONL format — content is wrapped in JSON
- When uncertain if something is stale, keep it (conservative approach)
- MEMORY.md is loaded in main sessions — keep it focused and relevant
- The skill is a workflow, not a binary — adapt to your setup

## Contributing

PRs welcome! Ideas for improvement:
- Better heuristics for "what's worth remembering"
- Alternative search methods
- Automation scripts for different platforms
- Integration with vector DBs for semantic search

GitHub: https://github.com/stewnight/rem-sleep-skill
