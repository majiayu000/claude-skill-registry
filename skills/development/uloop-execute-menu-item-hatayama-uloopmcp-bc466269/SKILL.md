---
name: uloop-execute-menu-item
description: 'Execute Unity MenuItem via uloop CLI. Use when you need to: (1) Trigger
  menu commands programmatically, (2) Automate editor actions (save, build, refresh),
  (3) Run custom menu items defined in scripts'
---

---
name: uloop-execute-menu-item
description: Execute Unity MenuItem via uloop CLI. Use when you need to: (1) Trigger menu commands programmatically, (2) Automate editor actions (save, build, refresh), (3) Run custom menu items defined in scripts.
---

# uloop execute-menu-item

Execute Unity MenuItem.

## Usage

```bash
uloop execute-menu-item --menu-item-path "<path>"
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--menu-item-path` | string | - | Menu item path (e.g., "GameObject/Create Empty") |
| `--use-reflection-fallback` | boolean | `true` | Use reflection fallback |

## Examples

```bash
# Create empty GameObject
uloop execute-menu-item --menu-item-path "GameObject/Create Empty"

# Save scene
uloop execute-menu-item --menu-item-path "File/Save"

# Open project settings
uloop execute-menu-item --menu-item-path "Edit/Project Settings..."
```

## Output

Returns JSON with execution result.

## Notes

- Use `uloop get-menu-items` to discover available menu paths
- Some menu items may require specific context or selection
