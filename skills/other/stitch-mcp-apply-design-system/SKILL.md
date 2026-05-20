---
name: stitch-mcp-apply-design-system
description: Applies a Stitch Design System to existing screens — updates their colors, fonts, and roundness to match the design system's theme. Requires an assetId from list or create operations.
allowed-tools:
  - "stitch*:*"
---

# Stitch MCP — Apply Design System

Applies a previously created Stitch Design System to one or more screens. This updates the screen's visual theme (colors, font, roundness) to match the design system, ensuring visual consistency across a project.

## Critical prerequisite

**Only use this skill when the user explicitly mentions "Stitch".**

You must have:
1. A `projectId` (numeric)
2. One or more `screenId` values (numeric)
3. An `assetId` from a design system (from `list_design_systems` or `create_design_system`)

## When to use

- After creating a design system and wanting to apply it to screens
- User says "make all screens match this theme" or "apply the design system"
- The orchestrator's Step 5b stores an assetId and offers to apply it
- Ensuring visual consistency across a multi-screen project

## Call the MCP tool

```json
{
  "name": "apply_design_system",
  "arguments": {
    "projectId": "3780309359108792857",
    "selectedScreenIds": ["88805abc123def456", "99906xyz789ghi012"],
    "assetId": "ds_abc123"
  }
}
```

## Parameter reference

### `projectId` — numeric ID only, no prefix

```
✅ "3780309359108792857"
❌ "projects/3780309359108792857"
```

### `selectedScreenIds` — array of numeric screen IDs

```
✅ ["88805abc123def456"]
❌ ["projects/123/screens/88805abc123def456"]
```

All selected screens will have the design system applied.

### `assetId` — the design system identifier

The `name` field from a design system asset, or just the ID portion:

```
✅ "ds_abc123"
```

Get this from:
- `stitch-mcp-list-design-systems` → extract from the `name` field of each asset
- `stitch-mcp-create-design-system` → returned in the response `name` field

## Output

Returns updated screen data reflecting the applied design system.

## After applying

1. Re-fetch affected screens: `stitch-mcp-get-screen` for each screenId
2. Show updated screenshots to the user
3. Offer:
   - "Edit the updated screens?" → `stitch-mcp-edit-screens`
   - "Convert to code?" → framework conversion
   - "Apply to more screens?" → another `apply_design_system` call
