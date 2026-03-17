---
description: Show progress for active increments with task/AC completion. Use when saying "show progress", "status", or "how far along".
argument-hint: "[incrementId]"
---

# Increment Progress

## Project Overrides

!`s="progress"; for d in .specweave/skill-memories .claude/skill-memories "$HOME/.claude/skill-memories"; do p="$d/$s.md"; [ -f "$p" ] && awk '/^## Learnings$/{ok=1;next}/^## /{ok=0}ok' "$p" && break; done 2>/dev/null; true`

## Hook Execution (Default)

This command is intercepted by the **UserPromptSubmit hook** for instant execution (<10ms). The hook reads from `.specweave/state/dashboard.json` cache.

**CRITICAL**: The hook output in `<system-reminder>` is ALREADY FORMATTED for the user. You MUST:
1. Present the hook output VERBATIM — copy it exactly as-is
2. Do NOT reformat into a markdown table
3. Do NOT re-summarize or paraphrase the data
4. Do NOT add interpretation unless the user asks a follow-up question
5. If the user asks "what should I work on next?" THEN add recommendations

## CLI Fallback

If hook output isn't displayed (rare), execute:

```bash
specweave status --verbose
```

## Arguments

- `/sw:progress` - Show all active increments
- `/sw:progress 0042` - Show specific increment details (partial ID match supported)

## Related Commands

- `/sw:done <id>` - Close increment after review
- `/sw:increment` - Start new work
