---
name: uloop-get-menu-items
description: 'Retrieve Unity MenuItems via uloop CLI. Use when you need to: (1) Discover
  available menu commands in Unity Editor, (2) Find menu paths for automation, (3)
  Prepare for executing menu items programmati'
---

---
name: uloop-get-menu-items
description: Retrieve Unity MenuItems via uloop CLI. Use when you need to: (1) Discover available menu commands in Unity Editor, (2) Find menu paths for automation, (3) Prepare for executing menu items programmatically.
---

# uloop get-menu-items

Retrieve Unity MenuItems.

## Usage

```bash
uloop get-menu-items [options]
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--filter-text` | string | - | Filter text |
| `--filter-type` | string | `contains` | Filter type: `contains`, `exact`, `startswith` |
| `--max-count` | integer | `200` | Maximum number of items |
| `--include-validation` | boolean | `false` | Include validation functions |

## Examples

```bash
# List all menu items
uloop get-menu-items

# Filter by text
uloop get-menu-items --filter-text "GameObject"

# Exact match
uloop get-menu-items --filter-text "File/Save" --filter-type exact
```

## Output

Returns JSON array of menu items with paths and metadata.

## Notes

Use with `uloop execute-menu-item` to run discovered menu commands.
