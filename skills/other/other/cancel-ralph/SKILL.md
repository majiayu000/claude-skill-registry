---
name: cancel-ralph
description: Codex-compatible cancel command for Ralph loop state, preserving the original command name.
---

# cancel-ralph

This is a compatibility version of the Claude `cancel-ralph` command for Codex.
It only manages the local `compat` loop state used by `ralph-loop --engine compat`.

## Script

- Script path: `scripts/cancel-ralph.ps1`

## Usage

```powershell
$codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
$script = Join-Path $codexHome 'skills/cancel-ralph/scripts/cancel-ralph.ps1'
powershell -ExecutionPolicy Bypass -File $script
```

## Vibe compatibility

- Safe in `/vibe` routed sessions as a direct execution tool.
- Uses the same state file path policy as `ralph-loop`.
- Not used by `ralph-loop --engine open` (external open-ralph-wiggum backend).

## Behavior

- If no active Ralph state exists, reports `No active Ralph loop found.`
- If active state exists, removes it and reports current iteration.

