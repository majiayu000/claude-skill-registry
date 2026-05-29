---
name: cask
description: Async via cask, end turn immediately; use only when user explicitly delegates to Codex (ask/@codex/let codex/review); NOT for questions about Codex itself.
metadata:
  short-description: Ask Codex asynchronously via cask
  managed-by: ccb-installer
  template-variant: powershell
---

# Ask Codex (Async)

Send the user’s request to Codex asynchronously.

## Execution (MANDATORY)

```
Bash(@"
$ARGUMENTS
"@ | cask, run_in_background=true)
```

## CRITICAL Rules

- Always use `run_in_background=true`.
- After running `cask`, say “Codex processing...” and immediately end your turn.
- Do not wait for results or check status in the same turn.

## Notes

- If it fails, check backend health with `cping`, or start it with `ccb up codex`.
- For short 1-liners you can also do: `Bash(cask "…", run_in_background=true)` (but prefer here-string for arbitrary text).
- For a more complete pattern (including multiline): `../docs/async-ask-pattern.md`
