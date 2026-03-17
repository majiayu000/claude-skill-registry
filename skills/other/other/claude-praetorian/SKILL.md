---
name: claude-praetorian
description: Context preservation with cross-session memory — hooks prompt compaction at high-impact moments, siblings enrich what gets saved
triggers: [PreToolUse, PreCompact, PostToolUse, SubagentStop]
---

# Praetorian Plugin

Context guard. Saves and restores valuable context at the right moments — before planning, after research, when subagents complete.

## Hooks

| Hook | When | Action |
|------|------|--------|
| **PreToolUse(EnterPlanMode)** | Before planning | Lists prior compactions, suggests restoring |
| **PreCompact** | Before context resets | Prompts to save decisions/insights/findings |
| **PostToolUse(WebFetch/WebSearch)** | After web research | Prompts to compact as `web_research` |
| **SubagentStop** | After subagent completes | Prompts to compact as `task_result` |

## Commands

| Command | Description |
|---------|-------------|
| `/compact-praetorian [type] [title]` | Save current context |
| `/restore-praetorian [query]` | Load previous context |

## Workflows

### Compact (standalone)

1. Identify what's worth saving (research, decisions, patterns)
2. `praetorian_compact(type, title, key_insights, refs)`
3. Verify with `praetorian_restore(title)` to confirm it saved

### Compact (with siblings)

1. If **historian** active: `search_plans()` to check if past context already covers this
2. If **oracle** active: include any tool discoveries in `key_insights`
3. `praetorian_compact(type, title, key_insights, refs)`
4. If **vigil** active: files are also checkpointed via quicksave

### Restore (standalone)

1. `praetorian_restore()` — list recent compactions
2. `praetorian_restore("query")` — search for specific topic
3. Summarize findings for the current task

### Restore (with siblings)

1. `praetorian_restore("query")` — load praetorian context
2. If **historian** active: `search_conversations("query")` for broader session history
3. If **oracle** active: `search("query")` for tools relevant to the restored context
4. Combine all sources into a unified briefing

## Sibling Synergy

| Sibling | Value | How |
|---------|-------|-----|
| **Historian** | Past plans surface during planning compactions | `search_plans()` enriches pre-plan hook |
| **Oracle** | Tool discoveries included in compactions | Oracle results added to `key_insights` |
| **Gladiator** | Observations inform what to compact | Failure patterns highlight important context |
| **Vigil** | Files checkpointed alongside context | Quicksave protects files during compaction |

## Requires

```
claude mcp add praetorian -- npx claude-praetorian-mcp
```
