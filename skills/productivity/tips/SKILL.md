---
name: tips
description: Use when starting a Claude Code session, feeling overwhelmed by context, or needing workflow tips. Triggers on "how do I manage sessions", "context getting long", "remind me".
---

# Claude Code Session Tips

Quick reference for effective Claude Code usage.

## Session Management

| Action            | How                                                                   |
| ----------------- | --------------------------------------------------------------------- |
| Clear context     | `/clear` (rename first with `/rename` for easy return)                |
| Resume session    | `claude --resume <session-id>`                                        |
| Fork session      | `claude --continue --fork-session` (branch off without modifying original) |
| Clear input area  | `Esc Esc` (double-tap)                                                |
| Clear single line | `Ctrl+U` (shell shortcut)                                             |
| Stash input       | `Ctrl+S` - saves draft, auto-restores after next submit ([#14740][1], [source][2]) |
| Optimize Rules    | `/claude-md-improver`                                                              |

[1]: https://github.com/anthropics/claude-code/issues/14740
[2]: https://x.com/adocomplete/status/2014047394585825296

## Context Hygiene

- `/clear` aggressively - long contexts slow responses
- `/rename` before clearing to make sessions findable

## Quota Management (Max Subscription)

**Key insight:** Context size counts toward your quota. Each turn re-sends the entire conversation history.

| Context size | Per-turn cost |
|--------------|---------------|
| 20k (fresh)  | 1x            |
| 100k         | 5x            |
| 180k         | 9x            |

**The rule:** If your next question doesn't need previous context, `/clear` first.

**Mid-work one-off questions:**
- Option A: Ask parent to spawn subagent → still costs 1 parent turn
- Option B: New Ghostty tab → cheaper IF you use the knowledge implicitly without pasting back
- Best: New tab, absorb answer yourself, continue in parent with informed instructions

## Auto-Compact Buffer ([source][3], [docs][4])

**Formula:** `buffer = 13k + maxOutputTokens`

| `CLAUDE_CODE_MAX_OUTPUT_TOKENS` | Buffer | Effective Context |
|---------------------------------|--------|-------------------|
| 22k (more context)              | 35k    | ~165k             |
| 32k (default)                   | 45k    | ~155k             |
| 64k (max)                       | 77k    | ~123k             |

Trade-off: lower output tokens = more context but shorter max responses.

[3]: https://x.com/bcherny/status/2012670336362492296
[4]: https://code.claude.com/docs/en/settings

## Theming & Appearance

**Toggle CC's syntax theme:** `/config` → Theme → `Ctrl+T`

- **Syntax highlighting** (code colors): Controlled by toggle. Disabling uses terminal's colors.
- **Diff backgrounds** (red/green): Hardcoded. Cannot be themed ([#1302][5], [#14144][6]).

[5]: https://github.com/anthropics/claude-code/issues/1302
[6]: https://github.com/anthropics/claude-code/issues/14144
