---
name: memory-engine
description: Memory management system for Claude Code — Student Loop, Smart Context, Auto Learn, Session Handoff, Correction Cycle. Triggered by memory commands (/save, /reflect, /handoff, /check) or memory-related questions. Not for general programming tasks.
---

# Memory Engine v1.5.2

A memory and learning system for Claude Code, built with hooks and markdown.

## Modules

### 1. Smart Context

Auto-detects the current project from your working directory and loads its memory.

- Resolves per-project memory directory automatically — no hardcoded paths
- Implementation: `~/.claude/scripts/hooks/session-start.js`
- Config: `references/smart-context.md`

### 2. Auto Learn (Pitfall Detection)

Detects pitfall patterns before context compression — retries, errors followed by fixes, user corrections.

- Saves both the problem and the fix to `~/.claude/skills/learned/`
- Same mistake 3+ times across different days → suggests writing it into permanent rules
- Implementation: `shared-utils.js` → `detectPitfalls()` + `savePitfalls()`

### 3. Student Loop (/reflect)

8-step learning cycle. First 3 steps are automatic (every session). Last 5 via `/reflect`.

1. Takes notes — records what was done, files changed, decisions made
2. Links them — tags the project, connects to previous notes
3. Spots patterns — scans for pitfall signals

There is no real "end" to a Claude Code conversation. Memory Engine saves at three points:
- **Every 20 messages** (`mid-session-checkpoint`) — most reliable, self-counted
- **Before context compression** (`pre-compact`) — pitfall detection runs here, context is fullest
- **When conversation ends** (`session-end`) — best-effort, not guaranteed to fire

You don't need to remember to run any command before closing.
4. Review — read past 7 days, mark useful vs outdated
5. Refine — 4-question decision tree (Keep? Condense? Already covered? Delete as last resort)
6. Re-study — re-analyze cleaned data for buried patterns
7. Slim down — list removable items, wait for user confirmation
8. Wrap up — produce a report

### 4. Session Handoff (/handoff)

Pass context between Claude Code windows without losing progress.

- `/handoff` saves a `handoff-*.md` file with progress, decisions, unfinished tasks
- Next session auto-detects it on startup (`session-start.js`)
- Mid-conversation detection via `memory-sync.js`
- Each handoff is shown once, tracked by `.handoff-read.json`

### 5. Correction Cycle (/analyze)

Learns from user corrections — mistakes that don't show up in error logs.

- **Analyze** (`/analyze`) — compare user's edits against rules, log missed rules, distill new ones
- **Correct** (auto, before tasks) — scan the error list as a reminder
- **Reflect** (`/reflect` step 6) — same mistake 3+ times → upgrade to hard rule

## Hooks

| Hook | File | What it does |
| :--- | :--- | :----------- |
| SessionStart | session-start.js | Load last summary + project memory + pending handoffs + pitfall review + /reflect reminder |
| SessionEnd | session-end.js | Save summary + project index + backup (best-effort, may not fire) |
| PreCompact | pre-compact.js | Snapshot + pitfall detection + backup — the real safety net |
| UserPromptSubmit | memory-sync.js | Cross-session memory change detection + handoff detection |
| UserPromptSubmit | mid-session-checkpoint.js | Checkpoint every 20 messages |
| PreToolUse(Write) | write-guard.js | Sensitive file write warning |
| PreToolUse(Bash) | pre-push-check.js | Safety check before git push |

Shared logic between `session-end.js` and `pre-compact.js` is extracted into `shared-utils.js`.

## Commands (36 files, 18 pairs EN + ZH)

| EN | ZH | Function |
| :- | :- | :------- |
| /save | /存記憶 | Save memory — auto-dedup, route to correct file |
| /reload | /讀取 | Load memory into current conversation |
| /todo | /待辦 | Cross-project task tracking |
| /backup | /備份 | Push local memory to GitHub |
| /sync | /同步 | Bidirectional sync |
| /handoff | /交接 | Session handoff — pass progress to next window |
| /diary | /回顧 | Generate reflection diary |
| /reflect | /反思 | Analyze pitfalls, find patterns |
| /learn | /學習 | Manually save a pitfall |
| /analyze | /分析 | Record corrections into error notebook |
| /correct | /訂正 | Review error notebook anytime |
| /check | /健檢 | Quick health scan |
| /full-check | /大健檢 | Full audit |
| /memory-health | /記憶健檢 | Memory file stats + capacity warnings |
| /memory-search | /搜尋記憶 | Keyword search across all memory files |
| /recover | /想起來 | Restore memory from GitHub backup |
| /compact-guide | /壓縮建議 | When to compact and when not to |
| /overview | /全覽 | List all available commands |

## File Structure

```text
~/.claude/
  scripts/hooks/
    session-start.js         # Load recall + smart-context + handoff
    session-end.js           # Save summary + backup (best-effort)
    pre-compact.js           # Pre-compression snapshot + pitfall detection + backup
    shared-utils.js          # Shared functions (transcript, pitfall, backup)
    memory-sync.js           # Cross-session sync + handoff detection
    mid-session-checkpoint.js
    write-guard.js
    pre-push-check.js
  sessions/
    {date}-{id}-session.md   # Session summaries
    {date}-{id}-compact.md   # Pre-compact snapshots
    diary/                   # Reflection diaries
  commands/
    save.md / 存記憶.md       # ...15 pairs
    handoff.md / 交接.md
  skills/learned/memory-engine/
    SKILL.md                 # This file
    references/
      smart-context.md       # Project detection rules
      auto-learn.md          # Pitfall detection rules
```

## Core Principles

### Test what you build

- After creating any hook or feature, always run a test to confirm it works
- "Written" does not mean "done" — see actual output before marking complete

### /reflect 4-question decision tree

1. Does it serve the main purpose? → No → remove
2. Can it be condensed? → Yes → replace with refined version
3. Already covered by an existing rule? → Yes → don't duplicate
4. Delete is the last resort → only if Q1-Q3 don't apply

## Troubleshooting

### MEMORY.md over 200 lines with no warning

- **Cause:** Didn't check line count before writing
- **Fix:** Run `wc -l` before every write. Over 170 lines → move old content to standalone files first

### Memory saved but next session doesn't know

- **Cause:** Content written directly into MEMORY.md instead of creating a pointer
- **Fix:** MEMORY.md holds pointers only. Details go in `memory/*.md`

### Backup push fails

- **Cause:** Conflicts in the memory repo or expired auth
- **Fix:** Run `git pull` first, resolve conflicts if any

## References

- `references/smart-context.md` — Project detection rules
- `references/auto-learn.md` — Pitfall detection rules + auto-learn flow
