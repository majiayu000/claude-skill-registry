---
name: uloop-find-game-objects
description: 'Find GameObjects with search criteria via uloop CLI. Use when you need
  to: (1) Locate GameObjects by name pattern, (2) Find objects by tag or layer, (3)
  Search for objects with specific component type'
---

---
name: uloop-find-game-objects
description: Find GameObjects with search criteria via uloop CLI. Use when you need to: (1) Locate GameObjects by name pattern, (2) Find objects by tag or layer, (3) Search for objects with specific component types.
---

# uloop find-game-objects

Find GameObjects with search criteria.

## Usage

```bash
uloop find-game-objects [options]
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--name-pattern` | string | - | Name pattern to search |
| `--search-mode` | string | `Contains` | Search mode: `Exact`, `Path`, `Regex`, `Contains` |
| `--required-components` | array | - | Required components |
| `--tag` | string | - | Tag filter |
| `--layer` | string | - | Layer filter |
| `--max-results` | integer | `20` | Maximum number of results |
| `--include-inactive` | boolean | `false` | Include inactive GameObjects |

## Examples

```bash
# Find by name
uloop find-game-objects --name-pattern "Player"

# Find with component
uloop find-game-objects --required-components Rigidbody

# Find by tag
uloop find-game-objects --tag "Enemy"

# Regex search
uloop find-game-objects --name-pattern "UI_.*" --search-mode Regex
```

## Output

Returns JSON array of matching GameObjects with paths and components.
