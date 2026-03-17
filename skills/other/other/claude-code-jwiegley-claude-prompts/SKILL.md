---
name: claude-code
description: >
  Prime Claude Code sessions with proper use of installed plugins and tools:
  Claude-mem (persistent memory), git-ai-search (conversation context from git),
  Cozempic (context weight management), and PAL MCP (multi-model collaboration).
  Use at session start to establish good habits.
---

# Claude Code Session Priming

You have several powerful plugins and tools installed. Follow these protocols
throughout the session to make full use of them.

## 1. Claude-mem (Persistent Memory)

Claude-mem provides semantic memory across sessions via MCP tools. A context
index is delivered automatically at session start in a system reminder.

### Protocol: Search Before Re-Investigating

Before reading files or exploring code to understand something, **check memory
first**. Past sessions likely already recorded the answer.

```
1. search(query) -> scan the index for relevant observation IDs
2. timeline(anchor=ID) -> get surrounding context
3. get_observations([IDs]) -> fetch full details only for filtered IDs
```

Never fetch full details without filtering first. The 3-layer workflow provides
10x token savings.

### Protocol: Save After Significant Work

After completing any of the following, call `save_memory` to record it:

- **Discoveries**: codebase structure, how a system works, where key code lives
- **Decisions**: architectural choices, approach trade-offs, why option A over B
- **Completed work**: what was built/changed, the final state, key details
- **Bug findings**: root cause, fix applied, symptoms vs actual problem
- **Learnings**: gotchas, undocumented behavior, things that surprised you

Write memory entries as self-contained observations. Future sessions will see
the title and token cost in the context index, then decide whether to fetch
the full record. A good title and enough detail to be useful standalone are
key.

### Protocol: Use the Context Index

The session-start context index shows past observations with:
- ID, timestamp, type (bugfix/feature/decision/discovery/etc.)
- Title, token cost to read, tokens of work that produced it
- File associations

Trust this index for past decisions and learnings. Only fetch full observations
when you need implementation details, rationale, or debugging context. Critical
types (bugfix, decision) often merit detailed fetching.

### Skills: /claude-mem:make-plan and /claude-mem:do

These skills create implementation plans with documentation discovery and
execute plans using subagents. Use them for structured multi-step work.

## 2. git-ai-search (Conversation Context from Git)

git-ai tracks AI-generated code and the conversations that produced it.

### When to Use

- **Resuming work on a git repo**: Search for AI context on recent commits to
  understand what was done and why
- **Investigating unfamiliar code**: Check if AI sessions contributed to specific
  files or line ranges
- **Picking up a teammate's work**: Restore their conversation context
- **PR reviews**: Understand AI involvement in changes

### Key Commands

```bash
git-ai search --commit <sha>              # AI context for a commit
git-ai search --file <path> --lines 50-75 # AI context for specific lines
git-ai search --pattern "keyword"         # Search prompt content
git-ai continue --commit <sha>            # Restore session context
```

Use `/git-ai-search` to invoke the full skill when deeper investigation is
needed.

## 3. Cozempic (Context Weight Management)

Cozempic prevents context bloat, which causes degraded performance and lost
state (especially agent teams).

### Automatic Protection

The Cozempic guard daemon starts automatically at session init. It monitors
session size and can auto-prune before compaction kills agent teams.

### When to Use Proactively

- **Long sessions**: When you've been working for a while and context feels
  heavy, run `/cozempic diagnose` to check
- **Before agent teams**: Ensure guard mode is active before spawning teams
  with TeamCreate. Agent team state is lost when auto-compaction triggers.
- **After large file reads**: If you've read many large files, context may be
  bloated with stale content

### Quick Reference

| Situation | Action |
|-----------|--------|
| Check session size | `cozempic current` |
| Diagnose bloat | `/cozempic diagnose` |
| Prune and reload | `/cozempic treat` |
| Protect agent teams | Guard daemon (auto-started) |

### Prescriptions

- **gentle** (under 5MB): progress collapse, file dedup, metadata strip
- **standard** (5-20MB): + thinking blocks, tool trim, stale reads
- **aggressive** (over 20MB): + error collapse, document dedup, mega-block trim

## 4. PAL MCP (Multi-Model Collaboration)

PAL provides access to external models for second opinions, deep analysis, and
consensus building.

### When to Use

- **Complex debugging**: `mcp__pal__debug` for systematic root cause analysis
- **Architecture decisions**: `mcp__pal__consensus` to consult multiple models
- **Code review**: `mcp__pal__codereview` for structured review with expert
  validation
- **Before commits**: `mcp__pal__precommit` to validate changes
- **Deep analysis**: `mcp__pal__thinkdeep` for multi-step investigation

### Protocol: Choose the Right Tool

| Need | PAL Tool |
|------|----------|
| Second opinion on approach | `chat` |
| Systematic debugging | `debug` |
| Architecture/code analysis | `analyze` |
| Multi-model decision making | `consensus` |
| Code review | `codereview` |
| Pre-commit validation | `precommit` |
| Security audit | `secaudit` |
| Refactoring opportunities | `refactor` |
| Test generation | `testgen` |

## 5. Session Workflow Summary

### At Session Start

1. Read the Claude-mem context index (delivered automatically)
2. If resuming work in a git repo, consider `git-ai search` on recent commits
3. Search Claude-mem for relevant past work before starting new investigation

### During Work

1. Search memory before re-reading files or re-exploring code
2. Save significant findings, decisions, and completions to memory
3. Use PAL tools for complex analysis, debugging, and decisions
4. Monitor context health; use Cozempic if sessions run long

### Before Agent Teams

1. Verify Cozempic guard is running (check session-start logs)
2. If not running: `cozempic guard --threshold 50 -rx standard --interval 30`

### At Session End

1. Save any unsaved important findings to Claude-mem
2. For git repos, work will be captured by git-ai automatically on commit
