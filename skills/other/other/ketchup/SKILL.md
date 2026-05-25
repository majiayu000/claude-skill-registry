---
name: ketchup
description: "Easter-egg alias for /catchup. Same return-from-absence briefing, squeezier name. Use exactly like /catchup — all flags pass through unchanged."
effort: medium
disable-model-invocation: true
argument-hint: "[--since \"friday\"|\"2h\"|\"last-active\"|\"last-commit\"] [--sources github,git,linear,calendar] [--depth quick|standard|deep] [--focus prs,reviews-requested,mentions,impact]"
allowed-tools: Read, Grep, Glob, Bash, Write, WebFetch, Agent
---

# Ketchup 🍅 — alias for /catchup

You found the easter egg. `/ketchup` is a 1:1 alias for `/catchup` —
condiment-grade catch-up, no behavior change.

## Iron Laws

1. **Behave identically to `/catchup`** — this file adds nothing; it
   only forwards. Never diverge from the canonical skill.
2. **Pass `$ARGUMENTS` through verbatim** — same flags, same defaults.

## Execution

1. Read `${CLAUDE_PLUGIN_ROOT}/skills/catchup/SKILL.md`.
2. Execute that workflow exactly, with this invocation's `$ARGUMENTS`
   passed through unchanged (`--since`, `--sources`, `--depth`,
   `--focus` all behave the same).
3. In the brief's footer line, you may render the generator as
   `/ketchup 🍅` instead of `/catchup` — the only cosmetic difference.

That's it. One condiment, same nutrition.
