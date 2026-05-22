---
name: figma
description: >-
  Translate Figma designs into production code using the Figma MCP server.
  Covers the required get_design_context, get_metadata, get_screenshot flow,
  asset handling from localhost endpoints, variable extraction for design
  tokens, and code connect mapping. Trigger when a task involves Figma URLs,
  node IDs, design-to-code workflows, or Figma MCP troubleshooting.
allowed-tools:
  - Read
  - Bash
  - WebFetch
  - AskUserQuestion
metadata:
  version: "1.0.0"
  author: "platxa-skill-generator"
  tags:
    - guide
    - figma
    - design-to-code
    - mcp
  provenance:
    upstream_source: "figma"
    upstream_sha: "c0e08fdaa8ed6929110c97d1b867d101fd70218f"
    regenerated_at: "2026-02-04T22:10:00Z"
    generator_version: "1.0.0"
    intent_confidence: 0.62
---

# Figma MCP Design-to-Code

Translate Figma designs into production code through the Figma MCP server, following a strict fetch-then-implement workflow.

## Overview

The Figma MCP server exposes tools that return structured design data, screenshots, variable definitions, and code-connect mappings for any Figma node. Call MCP tools in a defined sequence, receive structured JSON and code scaffolding (defaulting to React + Tailwind), then adapt output to the target project's conventions.

**What you will learn:**

- The mandatory three-step fetch sequence before writing code
- When to use each MCP tool (`get_design_context`, `get_metadata`, `get_screenshot`, `get_variable_defs`)
- How to map Figma variables to project design tokens
- Asset handling rules for localhost image and SVG sources
- Code Connect mappings for component reuse across the codebase

**Prerequisites:**

- Figma MCP server (remote at `https://mcp.figma.com/mcp` or local Dev Mode)
- Valid `FIGMA_OAUTH_TOKEN` environment variable
- MCP client configured (see `references/figma-mcp-config.md`)

## Workflow

Every Figma-driven implementation follows this sequence. Do not skip steps.

### Step 1: Fetch Design Context

Call `get_design_context` with the Figma frame/layer URL. The server extracts the `node-id` from the link and returns structured design data plus React + Tailwind code.

```bash
get_design_context(url="https://www.figma.com/design/FILE_KEY/Name?node-id=123-456")
```

If the response is truncated, call `get_metadata` first to get a sparse XML outline of child node IDs, then re-call `get_design_context` targeting specific children:

```bash
get_metadata(url="https://www.figma.com/design/FILE_KEY/Name?node-id=123-456")
get_design_context(url="https://www.figma.com/design/FILE_KEY/Name?node-id=789-012")
```

### Step 2: Capture Visual Reference

Call `get_screenshot` for the node variant being implemented:

```bash
get_screenshot(url="https://www.figma.com/design/FILE_KEY/Name?node-id=123-456")
```

Use the screenshot to verify layout, spacing, and visual hierarchy during implementation.

### Step 3: Download Assets and Implement

Only after Steps 1 and 2 are complete:

1. Download image/SVG assets from the MCP server response
2. If the server returns a `localhost` source for an image or SVG, use it directly -- do not create placeholders
3. Do not import new icon packages; all assets come from the Figma payload
4. Translate the React + Tailwind scaffold into the project's framework conventions
5. Replace Tailwind utility classes with project design-system tokens (`--color-primary`, `--spacing-md`)
6. Reuse existing components (buttons, inputs, typography) instead of duplicating
7. Validate against the Figma screenshot for 1:1 visual parity

### Step 4: Extract Design Variables (Optional)

Call `get_variable_defs` to list colors, spacing, and typography variables used in the selection. Map these to your project's token system:

```bash
get_variable_defs(url="https://www.figma.com/design/FILE_KEY/Name?node-id=123-456")
# Returns: { "colors": [{ "name": "Primary/500", "value": "#6366F1" }], ... }
```

### Step 5: Map Code Connect (Optional)

Use `get_code_connect_map` to check if a node already maps to an existing component, and `add_code_connect_map` to register new mappings:

```bash
get_code_connect_map(url="https://www.figma.com/design/FILE_KEY/Name?node-id=123-456")
# Returns: { "codeConnectSrc": "src/components/ui/Button.tsx", "codeConnectName": "Button" }

add_code_connect_map(nodeId="123-456", codeConnectSrc="src/components/ui/Card.tsx", codeConnectName="Card")
```

## Best Practices

### Do

- Always run the full fetch sequence: `get_design_context` -> `get_screenshot` -> implement
- Use `get_metadata` before `get_design_context` when nodes are large (100+ layers)
- Use `get_variable_defs` to align Figma variables with project tokens
- Reuse existing project components; check `get_code_connect_map` first
- Register new component mappings with `add_code_connect_map` after implementation
- Use the project's color system (`--color-*`), typography scale, and spacing tokens
- Validate final UI against the Figma screenshot for look and behavior

### Avoid

- Skipping `get_design_context` and going straight to implementation
- Treating MCP-generated React + Tailwind as final production code
- Importing new icon packages when assets are in the Figma payload
- Creating placeholder images when a `localhost` source URL is provided
- Hardcoding pixel values instead of using design-system tokens
- Duplicating existing components instead of checking code connect maps

## Common Questions

### Q: The `get_design_context` response is truncated?

**A**: Call `get_metadata` first to get the XML outline with child node IDs. Then re-call `get_design_context` on individual child nodes instead of the parent container.

### Q: How do I adapt the React + Tailwind output for Vue or Svelte?

**A**: Add a framework directive to the prompt: `"generate my Figma selection in Vue"` or `"in Svelte with TypeScript"`. The MCP server adjusts the scaffold accordingly.

### Q: The Figma MCP server returns a localhost URL for an image?

**A**: Use the localhost URL directly as the `src` attribute. The MCP server hosts assets at a local endpoint during the session. Never replace it with a placeholder or external URL.

### Q: How do I configure the MCP server for Claude Code?

**A**: See `references/figma-mcp-config.md` for the full config snippet, environment variable setup, and verification checklist.

## Examples

### Example 1: Implement a Card Component

```
User: Build the pricing card from https://figma.com/design/XYZ/App?node-id=42-100
Assistant:
  1. get_design_context(url="...?node-id=42-100")
     -> Returns Card JSX with Tailwind classes, 3 child layers
  2. get_screenshot(url="...?node-id=42-100")
     -> PNG showing card with title, price, feature list, CTA button
  3. get_variable_defs(url="...?node-id=42-100")
     -> colors: Primary/500=#6366F1, Gray/100=#F3F4F6
     -> spacing: card-padding=24px, card-gap=16px
  4. Check get_code_connect_map -> Button already mapped to src/components/ui/Button.tsx
  5. Translate: Replace Tailwind classes with project tokens, reuse Button component
  6. Compare screenshot with rendered output -> 1:1 match
```

### Example 2: Handle a Large Page Layout

```
User: Implement the dashboard layout from https://figma.com/design/ABC/Dashboard?node-id=1-200
Assistant:
  1. get_design_context(url="...?node-id=1-200")
     -> Response truncated (200+ layers)
  2. get_metadata(url="...?node-id=1-200")
     -> XML outline: Sidebar(node-id=1-201), Header(1-202), MainContent(1-203)
  3. get_design_context(url="...?node-id=1-201") -> Sidebar JSX
  4. get_design_context(url="...?node-id=1-202") -> Header JSX
  5. get_design_context(url="...?node-id=1-203") -> MainContent JSX
  6. get_screenshot for each section
  7. Compose layout, reuse existing grid system and components
```

## Output Checklist

- [ ] Ran `get_design_context` for every implemented node
- [ ] Captured `get_screenshot` for visual reference
- [ ] Downloaded all assets from MCP (no placeholder images)
- [ ] Used localhost URLs directly when provided by the server
- [ ] Replaced Tailwind utilities with project design-system tokens
- [ ] Reused existing project components (checked code connect map)
- [ ] Validated 1:1 visual parity against Figma screenshot
- [ ] No new icon packages imported (all icons from Figma payload)

## References

Load on demand when deeper configuration or tool details are needed:

- `references/figma-mcp-config.md` -- MCP server setup, env vars, verification, troubleshooting
- `references/figma-tools-and-prompts.md` -- full tool catalog with prompt patterns per tool
- `references/figma-implementation-rules.md` -- code translation rules, token mapping, asset handling
