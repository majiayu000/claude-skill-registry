---
name: stitch-mcp-edit-screens
description: Edits existing Stitch screens with text prompts — the iteration tool. Change colors, layout, content, or style without regenerating from scratch. Supports refinement loops via output_components suggestions.
allowed-tools:
  - "stitch*:*"
  - "Bash"
  - "Read"
  - "Write"
---

# Stitch MCP — Edit Screens

Edits one or more existing screens using a text prompt. This is the primary iteration tool — instead of regenerating a screen from scratch (60–180s), you can refine what you already have with targeted changes.

## Critical prerequisite

**Only use this skill when the user explicitly mentions "Stitch".**

You must have both a `projectId` AND at least one `screenId` before calling this. If you don't:
- List screens via `stitch-mcp-list-screens` to find screen IDs
- Parse from context: `projects/123/screens/456` → projectId: `123`, screenId: `456`

## When to use

- User wants to modify an existing Stitch screen (change colors, layout, content, style)
- After generation, user says "make it darker", "change the font", "move the nav to the side"
- The orchestrator's Step 5b offers "Edit this screen"
- Any iterative refinement on a Stitch design

## Call the MCP tool

```json
{
  "name": "edit_screens",
  "arguments": {
    "projectId": "3780309359108792857",
    "selectedScreenIds": ["88805abc123def456"],
    "prompt": "Change the background to dark mode (#09090B). Make the primary color indigo (#818CF8). Increase the font size of the header to 32px bold.",
    "deviceType": "DESKTOP",
    "modelId": "GEMINI_3_1_PRO"
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
❌ ["screens/88805abc123def456"]
```

Select one or more screens to edit. All selected screens receive the same edit instruction.

### `prompt` — the edit instruction

Apply the same quality bar as generation prompts:
- Be specific: "Change background to #09090B" not "make it darker"
- Name exact components: "the header navigation" not "the top part"
- Include values: hex colors, px sizes, specific content text
- One focused change per call produces better results than many changes at once

### `deviceType` — optional

Same enum as `generate_screen_from_text`: `MOBILE`, `DESKTOP`, `TABLET`, `AGNOSTIC`

### `modelId` — optional

| Value | Use when |
|-------|---------|
| `GEMINI_3_1_PRO` | **Recommended** — complex layouts, high fidelity |
| `GEMINI_3_FLASH` | Fast iteration, wireframes, simple changes |
| `GEMINI_3_PRO` | **Deprecated.** Still works but will be removed. Use `GEMINI_3_1_PRO` instead. |

## Handling `output_components`

The response may contain `output_components` with suggestions:

```json
{
  "outputComponents": [
    { "text": "I've updated the background color and adjusted contrast ratios." },
    { "suggestion": "Would you also like me to update the sidebar to match the dark theme?" }
  ]
}
```

**When you see suggestions:**
1. Present them to the user
2. If the user accepts: call `edit_screens` again with the suggestion as the new `prompt`
3. This creates a natural refinement loop — keep going until the user is satisfied

## Timing

Same as generation: 60–180 seconds is normal.
- Do NOT retry during this window
- Do NOT assume failure if it takes > 60 seconds
- Each call creates a new edit — retries mean duplicate edits

## After editing

1. Re-fetch the screen: `stitch-mcp-get-screen` with the same projectId and screenId
2. Show the updated screenshot to the user
3. Offer:
   - "Continue editing?" → another `edit_screens` call
   - "Generate variants of this version?" → `stitch-mcp-generate-variants`
   - "Convert to code?" → framework conversion workflow

## Anti-patterns

- **Never send vague edit prompts** — "make it better" will produce unpredictable results
- **Never use `projects/ID` format** for projectId or screenId — both must be numeric
- **Never batch unrelated edits** — "change the color AND completely redo the layout" works poorly
