---
name: stitch-mcp-list-screens
description: Lists all screens in a Stitch project. Use this after generate_screen_from_text to find the screenId of the newly generated screen, then call stitch-mcp-get-screen to retrieve it.
allowed-tools:
  - "stitch*:*"
---

# Stitch MCP — List Screens

Lists all screens contained within a specific Stitch project. You typically call this right after `generate_screen_from_text` to find the `screenId` of the screen that was just created.

## Critical prerequisite

**Only use this skill when the user explicitly mentions "Stitch".**

## When to use

- Immediately after `generate_screen_from_text` — to find the new screen's ID
- User wants to browse all screens in a project
- You need a `screenId` to call `get_screen`
- Checking what screens already exist before generating a new one

## Call the MCP tool

**Important: Use the `projects/ID` format — not the numeric ID alone.**

```json
{
  "name": "list_screens",
  "arguments": {
    "projectId": "projects/3780309359108792857"
  }
}
```

```
✅ "projects/3780309359108792857"
❌ "3780309359108792857"
```

## Output schema

```json
{
  "screens": [
    {
      "name": "projects/3780309359108792857/screens/88805abc123def456",
      "title": "Login Screen",
      "screenshot": {
        "downloadUrl": "https://storage.googleapis.com/..."
      },
      "deviceType": "MOBILE"
    }
  ]
}
```

## After listing

1. Identify the target screen (usually the most recently generated — last in the list)
2. Extract the numeric `screenId` from the `name` field:
   - `"projects/3780309359108792857/screens/88805abc123def456"` → screenId = `"88805abc123def456"`
3. Call `stitch-mcp-get-screen` with the numeric `projectId` and `screenId`

## ID format reminder

For the next call (`get_screen`), you need the **numeric IDs** for both project and screen:
- `projectId` → `3780309359108792857` (strip `projects/` prefix)
- `screenId` → `88805abc123def456` (strip `projects/.../screens/` prefix)
