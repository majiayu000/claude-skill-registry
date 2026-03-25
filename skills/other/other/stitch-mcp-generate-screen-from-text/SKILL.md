---
name: stitch-mcp-generate-screen-from-text
description: Generates a high-fidelity UI screen or wireframe from a text prompt using Stitch. This is the core text-to-UI generation tool — the heart of the Stitch workflow.
allowed-tools:
  - "stitch*:*"
---

# Stitch MCP — Generate Screen from Text

Generates a UI design screen from a structured text prompt. This is the central action in any Stitch workflow — everything before it (spec generation, prompt assembly) is preparation, and everything after it (screen retrieval, code conversion) is follow-through.

## Critical prerequisite

**Only use this skill when the user explicitly mentions "Stitch" or when called from an upstream skill (e.g. stitch-ideate, stitch-orchestrator).**

You must have a `projectId` before calling this. If you don't have one:
- Create a new project via `stitch-mcp-create-project`
- Or find an existing project via `stitch-mcp-list-projects`

## When to use

- User asks to "design", "generate", "create", or "make" a screen using Stitch
- The orchestrator has assembled a prompt via `stitch-ui-prompt-architect`
- User provides specific visual requirements and wants a Stitch-generated result

## Call the MCP tool

```json
{
  "name": "generate_screen_from_text",
  "arguments": {
    "projectId": "3780309359108792857",
    "prompt": "[Full structured prompt — see below]",
    "deviceType": "MOBILE",
    "modelId": "GEMINI_3_1_PRO"
  }
}
```

## Parameter reference

### `projectId` — numeric ID only, no `projects/` prefix
```
✅ "3780309359108792857"
❌ "projects/3780309359108792857"
```

### `prompt` — use the `[Context] [Layout] [Components]` structure
```
[Context & Style]
[Device] [Mode] [screen type] for [product]. [aesthetic]. [theme]. [colors]. [font].

[Layout]
[Describe the structural arrangement]

[Components]
[Specific named UI components with details]
```

For best results, use the `stitch-ui-prompt-architect` skill to assemble the prompt before calling this tool.

### `deviceType`
| Value | Use when |
|-------|---------|
| `MOBILE` | Mobile app, phone-sized UI (default if uncertain) |
| `DESKTOP` | Web dashboard, landing page, SaaS UI |
| `TABLET` | Tablet-specific layout |
| `AGNOSTIC` | Not tied to a specific device — responsive/fluid layout |

### `modelId`
| Value | Use when |
|-------|---------|
| `GEMINI_3_1_PRO` | **Recommended** — complex layouts, high fidelity |
| `GEMINI_3_FLASH` | Fast iteration, wireframes, simple changes |
| `GEMINI_3_PRO` | **Deprecated.** Still works but will be removed. Use `GEMINI_3_1_PRO` instead. |

## After generating

This tool returns session info but **not the actual screenshot/HTML**. To retrieve the design:
1. Call `stitch-mcp-list-screens` with `projects/[projectId]` to find the new screen
2. Call `stitch-mcp-get-screen` with the `projectId` and `screenId` to get the screenshot and HTML

## Prompt quality checklist

Before calling this tool, verify the prompt:
- [ ] Specifies device type consistently with `deviceType` parameter
- [ ] Names specific components (not "some buttons" — "primary 'Sign In' button")
- [ ] Includes colors (hex codes or clear color names)
- [ ] Uses realistic content (not Lorem Ipsum)
- [ ] Specifies light or dark mode explicitly

## Batch generation from full PRDs

When the prompt is a **complete PRD document** (product overview, design system, multiple screen specifications, build guide), Stitch will generate **multiple screens in a single call** — not just one. Stitch generates up to 10 screens per call. A PRD with 8 screen specs typically produces 5-7 screens automatically.

This is the same mechanism Stitch's web Ideate uses for "generate all screens". The PRD format acts as a comprehensive prompt that Stitch decomposes internally.

**How to use batch generation:**
1. Send the full PRD text as the `prompt` parameter
2. Stitch generates up to ~10 screens per call from a multi-screen PRD
3. Two possible outcomes depending on whether the MCP response times out:

   **If response returns with data:**
   - Check `output_components` for continuation suggestions (e.g. "Yes, make them all", "Generate remaining screens")
   - Automatically call `generate_screen_from_text` again with the suggestion text as the `prompt` — the user already initiated generation, no need to re-confirm
   - Repeat until no more `output_components` suggestions appear (max 3 continuation calls to prevent infinite loops)

   **If response returns empty (HTTP timeout):**
   - Generation is still running server-side — do NOT retry
   - Wait 90-120 seconds, then call `list_screens` to discover what was generated
   - If empty, wait another 60 seconds and retry the list call
   - Generate any missing screens individually with focused prompts referencing the PRD's design system

## Timing

Stitch generation takes 60–180 seconds for single screens and up to 5 minutes for multi-screen PRD generation. This is normal behavior, not a timeout.
- Do NOT retry during this window
- Do NOT assume failure if it takes > 60 seconds
- The MCP tool may return empty for long generations — check `list_screens` afterward
- If it fails: wait 90 seconds, check `list_screens`, retry ONCE max if nothing appeared
- Each call creates a new generation — retries mean duplicate screens

## References

- `examples/desktop.md` — Desktop dashboard prompts (SaaS analytics, admin panel)
- `examples/mobile.md` — Mobile app prompts (login, social feed, e-commerce)
