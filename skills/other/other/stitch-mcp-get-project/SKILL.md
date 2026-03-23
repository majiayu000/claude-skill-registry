---
name: stitch-mcp-get-project
description: Retrieves metadata for a specific Stitch project — title, theme, create/update time. Use to inspect a project before generating new screens. Do NOT use this if you already have a screenId — use stitch-mcp-get-screen instead.
allowed-tools:
  - "stitch*:*"
---

# Stitch MCP — Get Project

Retrieves full metadata for a specific Stitch project. Useful for understanding an existing project's theme and screen list before generating additional screens.

## Critical prerequisite

**Only use this skill when the user explicitly mentions "Stitch".**

**Do NOT call this if you already have both `projectId` AND `screenId`.** In that case, call `stitch-mcp-get-screen` directly — it's more efficient.

## When to use

- User provides a Stitch project URL and you need its details
- You need to know the existing design theme before generating new consistent screens
- Verifying a project exists before proceeding

## Step 1: Parse the project ID from context

The user may provide the project reference in several formats — always extract to the `projects/ID` format:

| Input format | → Argument for `get_project` |
|---|---|
| `3780309359108792857` (numeric) | `projects/3780309359108792857` |
| `projects/3780309359108792857` | `projects/3780309359108792857` (use as-is) |
| `https://stitch.withgoogle.com/projects/3780309359108792857` | Extract ID → `projects/3780309359108792857` |

## Step 2: Call the MCP tool

```json
{
  "name": "get_project",
  "arguments": {
    "name": "projects/3780309359108792857"
  }
}
```

## Output schema

```json
{
  "name": "projects/3780309359108792857",
  "title": "Analytics Dashboard",
  "createTime": "2024-11-10T09:00:00Z",
  "updateTime": "2024-11-15T10:30:00Z",
  "designTheme": {
    "colorMode": "LIGHT",
    "primaryColor": "#6366F1"
  },
  "screenInstances": [
    { "name": "projects/3780309359108792857/screens/88805..." }
  ]
}
```

## After getting the project

- Note the `designTheme` — use it to keep new screens visually consistent
- Note the `screenInstances` list — extract screenId values if you need to inspect specific screens
- Use `stitch-mcp-list-screens` for a richer view of the screen list including thumbnails
