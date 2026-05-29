---
name: layout
description: Create complex panel layouts for testing. Use patterns like "2H", "3V", "2x2", "1+2H" to quickly set up multi-panel configurations.
argument-hint: "<pattern> e.g. 2H, 3V, 2x2, 1+2H"
allowed-tools: Bash(curl:*)
---

# Create Panel Layout

Generate and apply complex panel layouts for testing the iOS/web grid system.

## Arguments

`$ARGUMENTS` should contain a layout pattern. Supported patterns:

| Pattern | Description |
|---------|-------------|
| `2H` | 2 panels side-by-side (horizontal split) |
| `2V` | 2 panels stacked (vertical split) |
| `3H` | 3 panels in a row |
| `3V` | 3 panels in a column |
| `2x2` | 4 panels in a 2x2 grid |
| `1+2H` | 1 panel left, 2 stacked on right |
| `1+2V` | 1 panel top, 2 side-by-side on bottom |
| `2+1H` | 2 stacked on left, 1 panel on right |
| `2+1V` | 2 side-by-side on top, 1 panel on bottom |
| `1+3` | 1 large left, 3 stacked on right |
| `3+1` | 3 stacked on left, 1 large right |
| `6` | 6 panels (2 rows of 3) |
| `clear` | Remove all panels (empty layout) |

If no pattern provided, default to `2H`.

## Steps

### 1. Parse the pattern

Determine how many panels are needed based on the pattern.

### 2. Get current plugins and start instances

```bash
# Get available plugins
curl -s http://localhost:47100/plugins
```

Use the `agent` plugin by default. Start as many instances as needed:

```bash
# Start a new agent instance (repeat as needed)
curl -s -X POST http://localhost:47100/plugins/agent/start
```

Track the instance IDs returned from each start call.

### 3. Generate the layout JSON

Build the layout tree based on the pattern. Each leaf needs:
- `type`: "leaf"
- `id`: unique string (e.g., "panel-1", "panel-2")
- `pluginName`: "agent"
- `instanceId`: the instance ID from step 2

For splits:
- `type`: "split"
- `id`: unique string
- `direction`: "horizontal" or "vertical"
- `children`: array of exactly 2 nodes
- `sizes`: array of 2 numbers that sum to 100 (e.g., [50, 50])

### 4. Apply the layout

```bash
curl -s -X PUT http://localhost:47100/layout \
  -H "Content-Type: application/json" \
  -d '{"layout": {"version": 1, "root": <generated-tree>}}'
```

## Layout Examples

### 2H (2 horizontal)
```json
{
  "version": 1,
  "root": {
    "type": "split",
    "id": "root",
    "direction": "horizontal",
    "sizes": [50, 50],
    "children": [
      {"type": "leaf", "id": "panel-1", "pluginName": "agent", "instanceId": "1"},
      {"type": "leaf", "id": "panel-2", "pluginName": "agent", "instanceId": "2"}
    ]
  }
}
```

### 3V (3 vertical)
```json
{
  "version": 1,
  "root": {
    "type": "split",
    "id": "root",
    "direction": "vertical",
    "sizes": [33, 67],
    "children": [
      {"type": "leaf", "id": "panel-1", "pluginName": "agent", "instanceId": "1"},
      {
        "type": "split",
        "id": "split-2",
        "direction": "vertical",
        "sizes": [50, 50],
        "children": [
          {"type": "leaf", "id": "panel-2", "pluginName": "agent", "instanceId": "2"},
          {"type": "leaf", "id": "panel-3", "pluginName": "agent", "instanceId": "3"}
        ]
      }
    ]
  }
}
```

### 2x2 (4 panel grid)
```json
{
  "version": 1,
  "root": {
    "type": "split",
    "id": "root",
    "direction": "vertical",
    "sizes": [50, 50],
    "children": [
      {
        "type": "split",
        "id": "top-row",
        "direction": "horizontal",
        "sizes": [50, 50],
        "children": [
          {"type": "leaf", "id": "panel-1", "pluginName": "agent", "instanceId": "1"},
          {"type": "leaf", "id": "panel-2", "pluginName": "agent", "instanceId": "2"}
        ]
      },
      {
        "type": "split",
        "id": "bottom-row",
        "direction": "horizontal",
        "sizes": [50, 50],
        "children": [
          {"type": "leaf", "id": "panel-3", "pluginName": "agent", "instanceId": "3"},
          {"type": "leaf", "id": "panel-4", "pluginName": "agent", "instanceId": "4"}
        ]
      }
    ]
  }
}
```

### 1+2H (1 left, 2 stacked right)
```json
{
  "version": 1,
  "root": {
    "type": "split",
    "id": "root",
    "direction": "horizontal",
    "sizes": [50, 50],
    "children": [
      {"type": "leaf", "id": "panel-1", "pluginName": "agent", "instanceId": "1"},
      {
        "type": "split",
        "id": "right-stack",
        "direction": "vertical",
        "sizes": [50, 50],
        "children": [
          {"type": "leaf", "id": "panel-2", "pluginName": "agent", "instanceId": "2"},
          {"type": "leaf", "id": "panel-3", "pluginName": "agent", "instanceId": "3"}
        ]
      }
    ]
  }
}
```

### 1+2V (1 top, 2 side-by-side bottom)
```json
{
  "version": 1,
  "root": {
    "type": "split",
    "id": "root",
    "direction": "vertical",
    "sizes": [50, 50],
    "children": [
      {"type": "leaf", "id": "panel-1", "pluginName": "agent", "instanceId": "1"},
      {
        "type": "split",
        "id": "bottom-row",
        "direction": "horizontal",
        "sizes": [50, 50],
        "children": [
          {"type": "leaf", "id": "panel-2", "pluginName": "agent", "instanceId": "2"},
          {"type": "leaf", "id": "panel-3", "pluginName": "agent", "instanceId": "3"}
        ]
      }
    ]
  }
}
```

### 1+3 (1 large left, 3 stacked right)
```json
{
  "version": 1,
  "root": {
    "type": "split",
    "id": "root",
    "direction": "horizontal",
    "sizes": [50, 50],
    "children": [
      {"type": "leaf", "id": "panel-1", "pluginName": "agent", "instanceId": "1"},
      {
        "type": "split",
        "id": "right-stack",
        "direction": "vertical",
        "sizes": [33, 67],
        "children": [
          {"type": "leaf", "id": "panel-2", "pluginName": "agent", "instanceId": "2"},
          {
            "type": "split",
            "id": "right-bottom",
            "direction": "vertical",
            "sizes": [50, 50],
            "children": [
              {"type": "leaf", "id": "panel-3", "pluginName": "agent", "instanceId": "3"},
              {"type": "leaf", "id": "panel-4", "pluginName": "agent", "instanceId": "4"}
            ]
          }
        ]
      }
    ]
  }
}
```

### 6 panels (2 rows of 3)
```json
{
  "version": 1,
  "root": {
    "type": "split",
    "id": "root",
    "direction": "vertical",
    "sizes": [50, 50],
    "children": [
      {
        "type": "split",
        "id": "top-row",
        "direction": "horizontal",
        "sizes": [33, 67],
        "children": [
          {"type": "leaf", "id": "panel-1", "pluginName": "agent", "instanceId": "1"},
          {
            "type": "split",
            "id": "top-right",
            "direction": "horizontal",
            "sizes": [50, 50],
            "children": [
              {"type": "leaf", "id": "panel-2", "pluginName": "agent", "instanceId": "2"},
              {"type": "leaf", "id": "panel-3", "pluginName": "agent", "instanceId": "3"}
            ]
          }
        ]
      },
      {
        "type": "split",
        "id": "bottom-row",
        "direction": "horizontal",
        "sizes": [33, 67],
        "children": [
          {"type": "leaf", "id": "panel-4", "pluginName": "agent", "instanceId": "4"},
          {
            "type": "split",
            "id": "bottom-right",
            "direction": "horizontal",
            "sizes": [50, 50],
            "children": [
              {"type": "leaf", "id": "panel-5", "pluginName": "agent", "instanceId": "5"},
              {"type": "leaf", "id": "panel-6", "pluginName": "agent", "instanceId": "6"}
            ]
          }
        ]
      }
    ]
  }
}
```

### clear (empty layout)
```json
{
  "version": 1,
  "root": null
}
```

## Output

Report:
1. Pattern interpreted
2. Number of instances started
3. Layout applied successfully
4. Tell user to check their iOS/web client
