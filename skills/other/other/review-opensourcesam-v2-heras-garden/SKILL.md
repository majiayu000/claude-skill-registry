---
name: review
description: Port of .claude/commands/review.md for Codex. Use MiniMax as the reviewer in place of Task.
---

# Review (Port)

Use this when the user requests `/review`.

1) Read `.claude/commands/review.md` for the full protocol.
2) Gather context (recent messages, file changes, work summary).
3) Since Task/subagents are not available, use MiniMax as the reviewer:
   - Prefer `mcp__MiniMax-Wrapper__coding_plan_general`.
   - Provide staged diff summary + key files + intent.
   - Ask for devil's-advocate review and call out risk areas.
4) Allow up to 3 back-and-forth rounds.
5) Report the final consensus only.
