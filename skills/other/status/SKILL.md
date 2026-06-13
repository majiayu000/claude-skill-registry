---
name: drill-status
description: Show drill-me learning progress — topics studied, cards due for review, weakest concepts, and what to study next. Use when the user asks what's due, how their learning is going, or for their drill-me status.
allowed-tools: "Read Glob Bash"
---

# drill-status

Report on the user's learning state. Read-only — no teaching, no ledger writes.

1. Run `date +%Y-%m-%d`.
2. Read `~/.drill-me/index.md` and every file in `~/.drill-me/topics/`.
   If the directory doesn't exist, say so and suggest `/drill:me <topic>` to start.
3. Print a compact report:
   - A table of topics: cards, due now, next due date, last session.
   - **Weak spots**: cards flagged `cw` (confident-wrong) or `leech`, and any card with
     stability under 2 days after 3+ reviews — name the concepts plainly.
   - **Recommendation**: the single best next action ("3 cards due in Rust lifetimes —
     a 10-minute review today beats 30 minutes on Friday").

Keep it under a screenful. No lectures, no science explainers — just the dashboard.
