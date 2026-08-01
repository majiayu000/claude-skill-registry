---
name: stitch-mcp-create-design-system-from-design-md
description: Creates a Stitch Design System from a DESIGN.md that was already uploaded with stitch-mcp-upload-design-md. Second half of a two-step pair — the upload must happen first.
allowed-tools:
  - "stitch*:*"
---

# Stitch MCP — Create Design System from DESIGN.md

Turns an uploaded DESIGN.md into a real Stitch Design System and displays it in the UI. This is step two of a pair — `stitch-mcp-upload-design-md` must have run first, because this tool consumes the screen instance that upload created.

Calling it without a prior upload fails: there's no screen instance to point at.

## Critical prerequisite

**Only use this skill when the user explicitly mentions "Stitch"** in their request. Never trigger Stitch operations silently during regular conversation.

## When to use

- Immediately after `stitch-mcp-upload-design-md` returns — always, as a pair
- Never on its own

## Step 1: Confirm you have the screen instance

You need two values from the upload step. If you didn't capture them, fetch them now with `get_project` (note: this one takes the `projects/` prefix):

```json
{
  "name": "get_project",
  "arguments": { "name": "projects/3780309359108792857" }
}
```

Take the newest entry in `screenInstances` and read off both `id` and `sourceScreen`.

## Step 2: Call the MCP tool

```json
{
  "name": "create_design_system_from_design_md",
  "arguments": {
    "projectId": "3780309359108792857",
    "selectedScreenInstance": {
      "id": "a1b2c3d4e5f6",
      "sourceScreen": "projects/3780309359108792857/screens/98b50e2ddc9943efb387052637738f61"
    },
    "deviceType": "DESKTOP"
  }
}
```

**Three different ID formats in one call.** This is the single easiest place to get it wrong:

| Field | Format | Example |
|-------|--------|---------|
| `projectId` | numeric only, no prefix | `3780309359108792857` |
| `selectedScreenInstance.id` | screen **instance** id — *not* the source screen id | `a1b2c3d4e5f6` |
| `selectedScreenInstance.sourceScreen` | full resource path, both prefixes | `projects/.../screens/...` |

`deviceType` is optional: `MOBILE`, `DESKTOP`, `TABLET`, or `AGNOSTIC`. Omit it and Stitch decides.

## Step 3: Confirm and capture the asset id

On success you get back a design system with an asset id in `assets/NUMERIC_ID` form. Store both forms: `apply_design_system` wants the bare numeric part, `generate_screen_from_text`'s `designSystem` param wants the full `assets/NUMERIC_ID` string.

Announce it:
> "Design system created from your DESIGN.md (asset `15996705518239280238`). Want me to apply it to existing screens, or use it for the next generation?"

## Step 4: Put it to work

- **Apply to existing screens** → `stitch-mcp-apply-design-system`
- **Use for new screens** → pass `designSystem: "assets/15996705518239280238"` to `generate_screen_from_text`

## ID format rules (critical — different tools need different formats)

| Tool | ID format required |
|------|-------------------|
| `create_design_system_from_design_md` | Numeric projectId + the screen-instance pair above |
| `upload_design_md` | Numeric only: `3780309359108792857` |
| `apply_design_system` | Numeric `assetId`, no `assets/` prefix |
| `generate_screen_from_text` | `designSystem` **does** take the `assets/` prefix |
| `get_project` | Full path: `projects/3780309359108792857` |

> Yes — `apply_design_system` wants the bare asset id while `generate_screen_from_text` wants it prefixed. Same identifier, two formats, depending on which tool you hand it to.

## Integration

- Preceded by `stitch-mcp-upload-design-md`, always
- Followed by `stitch-mcp-apply-design-system` or a generation call
- List what already exists with `stitch-mcp-list-design-systems`
