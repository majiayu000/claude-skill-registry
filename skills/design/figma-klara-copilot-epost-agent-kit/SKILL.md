---
name: figma
description: (ePost) Use when extracting Figma data, mapping design tokens to code, or comparing implementation against Figma designs across any platform (web, iOS, Android)
user-invocable: false

metadata:
  agent-affinity: [epost-muji, epost-fullstack-developer]
  keywords: [figma, design, tokens, mcp, figma-to-code]
  platforms: [all]
---

# Figma Integration Skill

Figma MCP integration patterns for klara-theme design-to-code workflows.

## When Active

- Working in `libs/klara-theme/`
- Using Figma MCP tools (`get_design_context`, `get_variable_defs`, etc.)
- Documenting components from Figma designs
- Mapping design tokens between Figma and klara-theme
- Validating implementations against Figma designs

## MCP Tool Reference

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `get_design_context(nodeId)` | Fetch React+Tailwind representation | **Always first** for any Figma node |
| `get_variable_defs(nodeId)` | Extract design tokens/variables | **Always second** after `get_design_context` |
| `get_screenshot(nodeId)` | Get visual reference image | **Required** for validation |
| `get_metadata(nodeId)` | Get XML node structure (IDs, names, positions) | **Only if** `get_design_context` output is truncated |

### Tool Usage Pattern

```
1. get_design_context(nodeId)  → design representation
2. get_variable_defs(nodeId)   → token extraction
3. get_screenshot(nodeId)      → visual reference
4. Convert to klara-theme patterns
5. Validate against screenshot
```

## Golden Rules

1. **Be explicit** — Specify exactly which tools and nodes you want. Do not ask vaguely for "tokens."
2. **Never implement from `get_metadata` alone** — Always follow with `get_design_context` for the nodes you are building.
3. **Treat `get_design_context` output as a representation** — It returns React+Tailwind; you must convert to klara-theme patterns (forwardRef, `theme-ui-label`, token mapping).
4. **Avoid large selections** — Work in small chunks. If truncated, use `get_metadata` to identify sub-nodes, then fetch each with `get_design_context`.
5. **Prefer reuse** — Check `src/lib/components/` before creating anything new.
6. **Always validate visually** — Call `get_screenshot` and compare against your implementation.

## Token Mapping

klara-theme uses a 3-layer token system:

| Layer | Location | Purpose |
|-------|----------|---------|
| Primitives | `_tokens/1_primitives/` | Raw values (colors, spacing, typography) |
| Themes | `_tokens/2_themes/` | Semantic tokens (light/dark) |
| Components | `_tokens/3_components/` | Component-specific tokens |

### Figma Variable → CSS Variable Mapping

Figma variables map to klara-theme CSS variables via `theme-constants.ts`:

```typescript
// Figma: "color/background/primary" → CSS: "--klara-bg-primary"
// Figma: "spacing/md" → CSS: "--klara-spacing-md"
```

When extracting tokens from `get_variable_defs`:
1. Identify the Figma variable name
2. Look up the corresponding CSS variable in `theme-constants.ts`
3. Map to the correct token layer

## Anti-Truncation Strategy

Large Figma selections may truncate. Handle with:

1. **Work in small chunks** — Select individual components, not entire frames
2. **Fallback pattern**:
   - If `get_design_context` truncates → call `get_metadata` for structure
   - Extract child node IDs from metadata
   - Call `get_design_context` on each child separately
3. **Progressive extraction** — Start with the parent, then drill into children

## Visual Validation

After implementation, always validate:

1. Call `get_screenshot(nodeId)` for the Figma design
2. Compare against your implementation visually
3. Check for:
   - Layout alignment
   - Spacing consistency
   - Color accuracy
   - Typography matching
   - State variations (hover, focus, disabled)

### Drift Categories

If differences found, categorize as:
- **Intentional**: Design evolved, implementation is correct
- **Bug**: Implementation error, needs fix
- **Enhancement**: Design improvement not yet implemented

## Aspect Files

| Aspect | Purpose |
|--------|---------|
| `references/extraction-procedure.md` | Step-by-step Figma data extraction with anti-truncation handling |

## Related Resources

- **klara-theme docs**: `libs/klara-theme/CLAUDE.md`
- **ui-lib-dev skill**: `ui-lib-dev` — Component pipeline (plan, implement, audit, fix, document)
- **Schemas**: `libs/klara-theme/figma-data/schema/`
  - `component-data.schema.json` — Figma component data structure
  - `component-mapping.schema.json` — Prop mapping structure
- **Manifest**: `libs/klara-theme/figma-data/manifest.json` — Component tracking

## Output Formats

### Component Data (`.figma.json`)

```json
{
  "componentKey": "button",
  "componentSetNodeId": "1:2592",
  "variants": [...],
  "tokens": {...},
  "extractedAt": "2025-01-15T10:00:00Z"
}
```

### Prop Mapping (`.mapping.json`)

```json
{
  "componentKey": "button",
  "props": {
    "variant": {
      "figmaProperty": "Type",
      "values": { "primary": "Primary", "secondary": "Secondary" }
    }
  }
}
```
