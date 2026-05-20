---
name: superclaude-framework-compat
description: Codex compatibility layer for SuperClaude /sc:* commands with vibe-adapted routing.
---

# superclaude-framework-compat

Compatibility bridge for migrating SuperClaude Framework workflows into Codex while preserving `sc:*` memory patterns.

## What This Provides

- Keeps SuperClaude source repository under `~/.codex/SuperClaude_Framework`.
- Builds a compatibility command map for all `src/superclaude/commands/*.md` entries.
- Provides a router script that accepts `/sc:*` tokens and outputs Codex-native routing guidance.
- Integrates with `/vibe` as the default orchestration path.

## Router

- Script: `scripts/sc-router.ps1`
- Map file: `command-map.json`

## Usage

```powershell
$codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
$router = Join-Path $codexHome 'skills/superclaude-framework-compat/scripts/sc-router.ps1'

# List mapped commands
powershell -ExecutionPolicy Bypass -File $router --list

# Show one mapped command
powershell -ExecutionPolicy Bypass -File $router --show /sc:implement

# Use command-style input
powershell -ExecutionPolicy Bypass -File $router /sc:implement continue migration and verify
```

## Vibe Compatibility

- Default route is `/vibe` for command execution in Codex.
- Supports unified memory by preserving `sc:*` command semantics in mapping.
- Uses direct-map / partial-map / unsupported status labels for strict compatibility boundaries.