---
name: stitch-mcp-generate-variants
description: Generates design variants of existing Stitch screens using the native variant API. Explore alternative layouts, color schemes, fonts, or content with configurable creativity levels.
allowed-tools:
  - "stitch*:*"
---

# Stitch MCP — Generate Variants

Generates alternative versions of existing screens using Stitch's native variant generation API. This is more efficient than the text-prompt approach (1 API call vs. 3) and offers fine-grained control over what aspects to vary.

## Critical prerequisite

**Only use this skill when the user explicitly mentions "Stitch".**

You must have both a `projectId` AND at least one `screenId` of an existing screen. Variants are always based on an existing design — you can't generate variants from scratch.

## When to use

- User wants to explore alternative versions of an existing screen
- After generation, user says "show me some variations" or "try different styles"
- The orchestrator's Step 5b offers "Generate variants"
- A/B testing — creating multiple options for stakeholder review

## Call the MCP tool

```json
{
  "name": "generate_variants",
  "arguments": {
    "projectId": "3780309359108792857",
    "selectedScreenIds": ["88805abc123def456"],
    "prompt": "Explore different color schemes while keeping the layout structure",
    "variantOptions": {
      "variantCount": 3,
      "creativeRange": "EXPLORE",
      "aspects": ["COLOR_SCHEME", "IMAGES"]
    },
    "deviceType": "DESKTOP",
    "modelId": "GEMINI_3_PRO"
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

The source screen(s) to generate variants from.

### `prompt` — optional guidance for variant direction

Provide context about what kind of variations the user wants. The `variantOptions` do the heavy lifting, but the prompt adds nuance.

### `variantOptions` — controls what and how much to vary

| Field | Type | Values | Description |
|-------|------|--------|-------------|
| `variantCount` | int | 1–5 | Number of variants to generate |
| `creativeRange` | enum | `REFINE`, `EXPLORE`, `REIMAGINE` | How much to deviate from the original |
| `aspects` | array | See below | Which design aspects to vary |

#### `creativeRange` mapping from user language

| User says | → creativeRange | What it does |
|-----------|----------------|-------------|
| "subtle changes", "minor tweaks", "polish" | `REFINE` | Small refinements, stays close to original |
| "alternatives", "different options", "explore" | `EXPLORE` | Meaningful differences while keeping the concept |
| "radical", "completely different", "reimagine" | `REIMAGINE` | Major departures from the original design |

#### `aspects` — what to vary

| Value | Varies | Keeps stable |
|-------|--------|-------------|
| `LAYOUT` | Structure, spacing, component arrangement | Colors, fonts, content |
| `COLOR_SCHEME` | Colors, gradients, contrast | Layout, fonts, content |
| `IMAGES` | Photography, illustrations, icons | Layout, colors, text |
| `TEXT_FONT` | Typography, font choices, sizes | Layout, colors, content |
| `TEXT_CONTENT` | Copy, labels, placeholder text | Layout, colors, fonts |

You can combine aspects: `["LAYOUT", "COLOR_SCHEME"]` varies both simultaneously.

### `deviceType` — optional

Same enum: `MOBILE`, `DESKTOP`, `TABLET`, `AGNOSTIC`

### `modelId` — optional

| Value | Use when |
|-------|---------|
| `GEMINI_3_PRO` | Higher quality variants, complex designs |
| `GEMINI_3_FLASH` | Faster iteration, simpler screens |

## Output

Returns new screens added to the project. Each variant appears as a separate screen in `list_screens`.

## After generating variants

1. Call `stitch-mcp-list-screens` to find all new variant screens
2. Call `stitch-mcp-get-screen` for each to get screenshots
3. Present side by side: "Here are your 3 variants: [screenshots]. Which one do you prefer?"
4. Once the user picks a winner, offer:
   - "Edit the chosen variant further?" → `stitch-mcp-edit-screens`
   - "Convert to code?" → framework conversion workflow
   - "Generate more variants from the winner?" → another `generate_variants` call

## Anti-patterns

- **Never generate variants without an existing screen** — you need a source design
- **Never use `projects/ID` format** for projectId or screenId — both must be numeric
- **Never set `variantCount` above 5** — the API caps at 5
