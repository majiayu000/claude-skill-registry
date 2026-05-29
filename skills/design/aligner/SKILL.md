---
name: aligner
description: This skill should be used when creating visual diagrams, flowcharts, or architecture visualizations that benefit from user feedback. It enables a visual feedback loop where the agent generates JSON diagrams, users edit them visually in a browser, and the agent reads back comments and changes. Triggers on requests like "draw a diagram", "create a flowchart", "visualize this flow", "let me see this visually", or when planning complex workflows that would benefit from visual iteration with the user.
---

# Aligner - Visual Feedback Loop for AI Agents

Generate flowcharts and diagrams that users can edit visually. Read their comments and iterate together.

## Prerequisites

Aligner must be running for visual editing. Check or start it:

```bash
# Check if running
curl -s http://localhost:3001/diagrams > /dev/null && echo "Aligner running" || echo "Not running"

# To start (user runs in separate terminals):
# Terminal 1: cd ~/dev/aligner/server && node index.js
# Terminal 2: cd ~/dev/aligner && npm run dev
# Browser: http://localhost:5173
```

If Aligner is not running, instruct the user to start it before proceeding.

## Workflow

1. **Generate diagram** → Write JSON to `~/.aligner/global/diagram-name.json`
2. **Notify user** → "View/edit your diagram at http://localhost:5173"
3. **Wait for feedback** → User drags nodes, adds comments
4. **Read comments** → Use the read-comments script
5. **Respond** → Update diagram or reply to comments
6. **Iterate** → Repeat until satisfied

## Creating a Diagram

Write a JSON file to `~/.aligner/global/` (for global diagrams) or `<repo>/.aligner/` (for repo-specific diagrams):

```json
{
  "version": "1.0",
  "name": "Descriptive Name",
  "type": "flowchart",
  "nodes": [
    {
      "id": "unique-id",
      "type": "rect",
      "label": "Node Label",
      "position": { "x": 100, "y": 100 },
      "size": { "width": 160, "height": 50 },
      "style": { "fill": "#dbeafe", "stroke": "#3b82f6", "cornerRadius": 8 }
    }
  ],
  "edges": [
    { "id": "e1", "from": "source-id", "to": "target-id", "type": "arrow", "label": "optional" }
  ],
  "metadata": { "description": "What this diagram shows" }
}
```

### Node Types

| Type | Shape | Use For |
|------|-------|---------|
| `rect` | Rectangle | Actions, steps, processes |
| `diamond` | Diamond | Decisions, conditionals |
| `circle` | Circle | Start/end points |

### Edge Types

| Type | Appearance |
|------|------------|
| `arrow` | Solid line with arrow |
| `dashed` | Dashed line (optional/async paths) |
| `line` | Solid line, no arrow |

### Color Palette

Use consistent colors for semantic meaning:

| Meaning | Fill | Stroke | Example |
|---------|------|--------|---------|
| Primary/Action | `#dbeafe` | `#3b82f6` | Main flow steps |
| Success | `#dcfce7` | `#22c55e` | Completion states |
| Decision | `#fef3c7` | `#f59e0b` | Conditionals |
| Error | `#fee2e2` | `#ef4444` | Failure paths |
| External | `#e0e7ff` | `#6366f1` | Third-party systems |
| Neutral | `#f3f4f6` | `#6b7280` | Secondary steps |
| User | `#fce7f3` | `#ec4899` | User actions |

## Reading User Feedback

To check for user comments on a diagram:

```bash
scripts/read-comments.py ~/.aligner/global/diagram-name.json
```

This outputs all nodes with comments in a readable format.

## Replying to Comments

To reply to a user comment, add to the node's `comments` array:

```json
{
  "id": "some-node",
  "label": "Some Step",
  "comments": [
    { "from": "user", "text": "Is this the right approach?" },
    { "from": "agent", "text": "Yes, this follows the existing pattern in the codebase." }
  ]
}
```

Always preserve existing comments when updating - append your reply, don't replace.

## Layout Guidelines

- **Vertical flow**: Top to bottom, 100-120px between rows
- **Horizontal flow**: Left to right, 200-250px between columns
- **Node sizes**: 150-180px width, 50-80px height (larger for multi-line labels)
- **Decision diamonds**: 140-160px width, 70-90px height
- **Use `\n`** for multi-line labels

## Example: Simple Auth Flow

```json
{
  "version": "1.0",
  "name": "Login Flow",
  "type": "flowchart",
  "nodes": [
    {
      "id": "start",
      "type": "circle",
      "label": "Start",
      "position": { "x": 180, "y": 30 },
      "size": { "width": 60, "height": 60 },
      "style": { "fill": "#dcfce7", "stroke": "#22c55e" }
    },
    {
      "id": "login-form",
      "type": "rect",
      "label": "Show Login Form",
      "position": { "x": 130, "y": 120 },
      "size": { "width": 160, "height": 50 },
      "style": { "fill": "#dbeafe", "stroke": "#3b82f6", "cornerRadius": 8 }
    },
    {
      "id": "validate",
      "type": "diamond",
      "label": "Valid?",
      "position": { "x": 145, "y": 210 },
      "size": { "width": 130, "height": 80 },
      "style": { "fill": "#fef3c7", "stroke": "#f59e0b" }
    },
    {
      "id": "success",
      "type": "rect",
      "label": "Dashboard",
      "position": { "x": 30, "y": 330 },
      "size": { "width": 140, "height": 50 },
      "style": { "fill": "#dcfce7", "stroke": "#22c55e", "cornerRadius": 8 }
    },
    {
      "id": "error",
      "type": "rect",
      "label": "Show Error",
      "position": { "x": 250, "y": 330 },
      "size": { "width": 140, "height": 50 },
      "style": { "fill": "#fee2e2", "stroke": "#ef4444", "cornerRadius": 8 }
    }
  ],
  "edges": [
    { "id": "e1", "from": "start", "to": "login-form", "type": "arrow" },
    { "id": "e2", "from": "login-form", "to": "validate", "type": "arrow" },
    { "id": "e3", "from": "validate", "to": "success", "type": "arrow", "label": "Yes" },
    { "id": "e4", "from": "validate", "to": "error", "type": "arrow", "label": "No" },
    { "id": "e5", "from": "error", "to": "login-form", "type": "dashed" }
  ],
  "metadata": { "description": "User authentication flow" }
}
```

## Tips

- Keep labels concise - detailed explanations go in comments
- Use the user's domain language in labels
- Start simple, let the user request more detail
- Always tell the user where to view the diagram after creating it
