---
name: spec-kit-vibe-compat
description: Compatibility router for /speckit.* workflows into /vibe-first Codex execution.
---

# spec-kit-vibe-compat

Bridge layer between spec-kit slash-command semantics and vibe orchestration.

## Usage

```powershell
$router = Join-Path $HOME '.codex/skills/spec-kit-vibe-compat/scripts/speckit-router.ps1'
powershell -ExecutionPolicy Bypass -File $router --list
powershell -ExecutionPolicy Bypass -File $router /speckit.implement continue migration
```

## Notes

- Keeps original `speckit` command memory model.
- Does not modify official spec-kit prompts.
- Produces `/vibe`-oriented execution guidance.
