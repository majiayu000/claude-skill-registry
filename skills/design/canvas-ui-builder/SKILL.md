---
name: canvas-ui-builder
description: Build PySide6 canvas UI components with the theme system and signal/slot rules. Use when: editing dialogs, panels, widgets, styles, or canvas UI behavior.
---

# Canvas UI Builder

Follow the theme system, slot rules, and panel coordination patterns for all UI work.

## Start Here

- `docs/agent/ui-theme.md`
- `docs/agent/ui-signal-slot.md`
- `.brain/docs/ui-standards.md`
- `.brain/docs/widget-rules.md`

## Core Rules (Non-Negotiable)

- Use theme tokens (`THEME_V2`, `TOKENS_V2`) for colors, spacing, typography, and radii.
- No hardcoded hex colors.
- All Qt slots must use `@Slot(...)`; no lambdas in signal connections.
- Use `DialogStyles` helpers for dialogs.
- Prefer `SignalCoordinator` and `PanelManager` for wiring.

## Minimal Slot Pattern

```python
from PySide6.QtCore import Slot

@Slot()
def _on_clicked(self) -> None:
    ...
```

## Common Paths

- UI widgets: `src/casare_rpa/presentation/canvas/ui/widgets/`
- Dialogs: `src/casare_rpa/presentation/canvas/ui/dialogs/`
- Panels: `src/casare_rpa/presentation/canvas/ui/panels/`
- Theme system: `src/casare_rpa/presentation/canvas/theme/`

## Tests

- UI tests: `tests/presentation/canvas/`
