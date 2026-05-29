---
name: lask
description: Send message to Claude pane (fire-and-forget). Use when relaying info back to Claude from Codex/Gemini/OpenCode.
metadata:
  short-description: Send a message to Claude via lask
  backend: claude
---

# lask (Send to Claude)

Send a message to the active Claude pane. Does not wait for reply.

## Prereqs (Backend)

- Requires a CCB session registry (created by `ccb up ...`) containing a `claude_pane_id`.
- `lask` must run in the same environment as `ccb` (WSL vs native Windows).

## Quick Start

- Preferred (works best on Windows too): `lask "$ARGUMENTS"`
- Multiline (optional): `lask <<'EOF'` … `EOF`

## Notes

- Fire-and-forget: only sends text, does not wait for Claude's response.
- If it fails to find the session/Claude pane, run `ccb up ...` (from within tmux/WezTerm) first.
