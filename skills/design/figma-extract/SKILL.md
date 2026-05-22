---
name: figma-extract
description: Extract design specifications and tokens from Figma files via MCP. Use when pulling design from Figma, extracting colors/typography, or converting Figma to spec. Triggers on keywords like "figma extract", "figma url", "figma tokens", "pull figma", "figma design".
allowed-tools: Read, Write
---

# Figma Extraction

Extract design specifications from Figma files using MCP integration.

## When to Use
- Figma URL provided for design extraction
- Need design tokens from Figma
- Converting Figma to implementation spec

## Quick Reference

### Workflow
1. Parse Figma URL (validate format)
2. Call MCP figma tools
3. Extract hierarchy (components, frames)
4. Extract design tokens (colors, text styles)
5. Return structured output
6. Used by `/design-spec` for full spec

### URL Format
```
https://www.figma.com/design/{fileKey}/{fileName}?node-id={nodeId}
```

### Arguments
| Arg | Required | Default | Description |
|-----|----------|---------|-------------|
| url | Yes | - | Figma design URL |
| output | No | markdown | markdown \| json |
| depth | No | 5 | Hierarchy depth 1-10 |
| timeout | No | 30 | Seconds |

### Output Structure
```markdown
## Component: {Name}

### Hierarchy
- Frame: {name}
  - Component: {name}
    - Text: {content}

### Design Tokens
#### Colors
- Primary: #XXXXXX
- Secondary: #XXXXXX

#### Typography
- Heading: {font} {size}/{lineHeight}
- Body: {font} {size}/{lineHeight}

#### Spacing
- Gap: {value}px
```

### Related
- **Role Skill:** `ux-designer`
- **Command:** `/figma-extract`
- **Used by:** `/design-spec`
- **MCP:** Requires figma MCP tools

## Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
