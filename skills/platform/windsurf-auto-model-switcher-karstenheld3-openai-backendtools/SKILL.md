---
name: windsurf-auto-model-switcher
description: Switch Windsurf Cascade AI models programmatically. Apply when needing to change models from workflows or scripts.
---

# Windsurf Auto Model Switcher

Switch Windsurf Cascade AI models programmatically using keyboard simulation.

## MUST-NOT-FORGET

- Requires custom keybindings (see SETUP.md)
- German keyboards: Use F-keys, not Ctrl+Alt (AltGr conflict)
- Model selector requires Windsurf window focus
- Auto-switching requires safety check (screenshot verification)

## Model Hints in STRUT

STRUT Strategy sections may include model hints:
```
├─ Strategy: Analyze requirements, design solution
│   - Opus for analysis, Sonnet for implementation
```

Model hints are recommendations - agent decides based on actual task.

## Prerequisites

1. Run SETUP.md to install keybindings
2. Restart Windsurf after setup

## Files

- `select-windsurf-model-in-ide.ps1` - Select a model by search query
- `windsurf-model-registry.json` - All available models and costs
- `update-model-registry/UPDATE_WINDSURF_MODEL_REGISTRY.md` - Workflow to update the registry

## Usage

```powershell
# Select Claude Sonnet 4.5
.\select-windsurf-model-in-ide.ps1 -Query "sonnet 4.5"

# Select Claude Opus 4.5 (Thinking)
.\select-windsurf-model-in-ide.ps1 -Query "opus 4.5 thinking"

# Select GPT-5.2 Low Reasoning
.\select-windsurf-model-in-ide.ps1 -Query "gpt-5.2 low"
```

## Model Registry

See `windsurf-model-registry.json` for all available models and their credit costs.

To update the registry, see `update-model-registry/UPDATE_WINDSURF_MODEL_REGISTRY.md`.

## Keybindings

Installed by SETUP.md:

- `Ctrl+Shift+F9` - Open model selector
- `Ctrl+Shift+F10` - Cycle to next model

## Troubleshooting

**Script types into editor**: Run SETUP.md and restart Windsurf.

**Model doesn't change**: Ensure Cascade panel is visible.

**Special characters (German keyboard)**: Use F-keys, not Ctrl+Alt.
