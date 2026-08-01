---
name: handoff-grok
description: Continue a task in xAI Grok Build using the shared Director handoff packet. Use when the user says to use Grok, requests a Grok review, or wants Grok Build to take over work started in Claude Code or Codex CLI.
user-invocable: true
---

# Handoff to Grok Build

Use the `session-relay` workflow so Grok receives the goal, decisions, Git
state, verification, and next steps without relying on another vendor's native
session ID.

```bash
ROOT="${CLAUDE_PROJECT_DIR:-${GROK_WORKSPACE_ROOT:-}}"
[[ -n "$ROOT" ]] || ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
RELAY="$ROOT/.director-mode/bin/director-relay"
[[ -x "$RELAY" ]] || RELAY="$HOME/.claude/bin/director-relay"

"$RELAY" create \
  --from <claude|codex> --to grok \
  --goal "..." --summary "..." --next "..."

"$RELAY" continue --to grok
```

The second command prints an interactive Grok command. Add `--run` only when
the user wants it launched immediately, or `--headless` for `grok -p`.

Grok also supports `grok import` for Claude Code sessions and automatically
reads Claude-compatible project assets. Treat those as a Claude→Grok shortcut,
not as a universal session format; keep the portable packet for three-way work.

Grok's approvals, permission rules, sandbox, network access, and hook trust stay
under Grok's native configuration. This skill does not change them.
