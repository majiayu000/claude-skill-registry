---
name: figma-design
version: 1.1.0
description: "[Design & Content] Extract design specifications from Figma designs using MCP server. Triggers on Figma URLs, design context extraction, or design-to-code workflows. Formerly also known as "figma-extract"."
infer: true
allowed-tools: Read, mcp__figma__get_file, mcp__figma__get_file_nodes
---

# Figma Design Context Extraction

## Summary

**Goal:** Extract design specifications (dimensions, layout, colors, typography) from Figma designs via MCP server for implementation.

| Step | Action | Key Notes |
|------|--------|-----------|
| 1 | Identify Figma URLs | Parse `node-id` from URL, convert hyphen to colon for API |
| 2 | Extract node data | Use `mcp__figma__get_file_nodes` (preferred over full file) |
| 3 | Summarize design context | Dimensions, layout, colors, typography, component structure |
| 4 | Token budget management | Single node: 500-2K tokens; AVOID full file (50K+) |

**Key Principles:**
- Always request specific nodes, never full files unless absolutely necessary
- Convert URL `node-id` format (hyphen) to API format (colon): `1-3` -> `1:3`
- Extract only essential properties; summarize children

## Purpose

Extract design specifications from Figma designs using the Figma MCP server. Used during planning workflows to gather detailed design context for implementation.

## Trigger

- Manually via `/figma-design` command
- Automatically when reading PBI/design-spec files containing Figma URLs (via hook)

## Prerequisites

1. **Figma MCP Server configured** - See `.mcp.README.md`
2. **Valid Figma URLs** - Format: `https://figma.com/design/{file_key}/...?node-id={node_id}`

## Workflow

### Step 1: Identify Figma URLs

Parse document content for Figma URLs:
```
https://figma.com/design/{file_key}/{name}?node-id={node_id}
```

**URL Format Notes:**
- `node-id` in URL uses hyphen: `1-3`
- API expects colon format: `1:3`
- Convert: `nodeId.replace('-', ':')`

### Step 2: Extract Node Data

```
# For specific node (preferred - token efficient)
mcp__figma__get_file_nodes file_key="{file_key}" node_ids="{node_id}"

# For full file (avoid unless necessary - high token usage)
mcp__figma__get_file file_key="{file_key}"
```

### Step 3: Summarize Design Context

| Property       | Source                                  |
| -------------- | --------------------------------------- |
| **Dimensions** | `absoluteBoundingBox.width/height`      |
| **Layout**     | `layoutMode`, `itemSpacing`, `padding*` |
| **Colors**     | `fills[].color` (r,g,b,a)               |
| **Typography** | `style.fontFamily/fontSize/fontWeight`  |
| **Children**   | `children[].name` (component structure) |

### Step 4: Token Budget Management

**Budget Targets:**
- Single node: 500-2,000 tokens
- Multiple nodes: <5,000 tokens total
- Full file: AVOID (can exceed 50K tokens)

**Optimization:** Always request specific nodes, extract only essential properties, summarize children.

## Output Format

```markdown
## Design Context: {Node Name}

**Dimensions:** {width}x{height}px
**Layout:** {layoutMode} | Spacing: {itemSpacing}px
**Colors:** {fill colors as rgba}
**Typography:** {fontFamily} {fontWeight} {fontSize}px

### Component Structure
- {child 1 name}
- {child 2 name}

### Key Design Decisions
- {extracted design pattern or decision}
```

## Error Handling

| Error              | Resolution                             |
| ------------------ | -------------------------------------- |
| `401 Unauthorized` | Check FIGMA_API_KEY in `.env.local`    |
| `404 Not Found`    | Verify file_key and node_id            |
| `403 Forbidden`    | Check file access permissions in Figma |
| Node not found     | Try parent node or verify URL          |

## Related

- `figma-extract` (deprecated, use this skill instead)
- `design-spec` - Design specification creation
- `ux-designer` - UI/UX design guidance

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**
- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
