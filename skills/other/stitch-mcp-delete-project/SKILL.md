---
name: stitch-mcp-delete-project
description: Permanently deletes a Stitch project and all its screens. Destructive — requires explicit user confirmation before calling.
allowed-tools:
  - "stitch*:*"
---

# Stitch MCP — Delete Project

Permanently deletes a Stitch project and all its screens, designs, and history. This action is irreversible.

## Critical prerequisite

**Only use this skill when the user explicitly mentions "Stitch".**

**This is a destructive action.** You MUST ask the user to confirm before calling `delete_project`. Never auto-delete.

## When to use

- User explicitly asks to delete a Stitch project
- Cleaning up test/scratch projects after confirming with the user
- The orchestrator offers project cleanup and the user accepts

## Step 1: Confirm the project

Show the user what they're about to delete:

1. Call `stitch-mcp-get-project` with `projects/[ID]` to get the project title and screen count
2. Present: "You're about to permanently delete **[title]** ([N] screens). This cannot be undone. Proceed?"
3. Only continue if the user explicitly confirms

## Step 2: Call the MCP tool

```json
{
  "name": "delete_project",
  "arguments": {
    "name": "projects/3780309359108792857"
  }
}
```

### `name` — full path with `projects/` prefix

```
✅ "projects/3780309359108792857"
❌ "3780309359108792857"
```

This follows the same format as `get_project` — both use `projects/ID`.

## After deleting

- Confirm: "Project **[title]** has been deleted."
- Offer: "Want to see your remaining projects?" → `stitch-mcp-list-projects`
- Do NOT attempt to access the deleted project's screens or data

## Anti-patterns

- **Never delete without explicit user confirmation** — even if the orchestrator suggests cleanup
- **Never delete multiple projects in a batch** without confirming each one
- **Never use numeric ID** — `delete_project` requires the full `projects/ID` path
