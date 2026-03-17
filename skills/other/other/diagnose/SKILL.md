---
name: diagnose
description: Analyze Claude Code session bloat — shows token count, context usage %, and bloat breakdown. Use when the user asks about session size, context usage, or when you notice the context window is getting full.
allowed-tools: Bash(cozempic *)
---

Run a diagnosis on the current session:

```bash
cozempic current --diagnose
```

The output includes:
- **Weight**: total session size in bytes and message count
- **Tokens**: exact token count (from usage data) or heuristic estimate
- **Context bar**: visual bar showing % of the 200K context window used
- **Vital signs**: progress ticks, file history snapshots, system reminders, thinking content, signatures, tool results
- **Message type breakdown**: bytes per message type
- **Top 10 largest messages**: biggest bloat contributors
- **Estimated savings by prescription**: what gentle/standard/aggressive would save

Always surface the token count and context % to the user. If context is above 60%, suggest running `/cozempic:treat` with a prescription recommendation:
- Under 5MB: `gentle`
- 5-20MB: `standard`
- Over 20MB: `aggressive`
