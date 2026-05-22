---
name: figma-extract
description: Extract design specifications and tokens from Figma files via MCP. Use when pulling design from Figma, extracting colors/typography, or converting Figma to spec. Triggers on keywords like "figma extract", "figma url", "figma tokens", "pull figma", "figma design".
infer: true
allowed-tools: Read, Write, mcp__figma__*
---

# Figma Extraction

Extract design specifications from Figma files using MCP integration.

## When to Use
- Figma URL provided for design extraction
- Need design tokens from Figma
- Converting Figma to implementation spec

## Pre-Workflow

### Activate Skills

- Activate `design-spec` skill for design extraction best practices

## Arguments

| Arg     | Required | Default  | Description          |
| ------- | -------- | -------- | -------------------- |
| url     | Yes      | -        | Figma design URL     |
| output  | No       | markdown | markdown \| json     |
| depth   | No       | 5        | Hierarchy depth 1-10 |
| timeout | No       | 30       | Seconds              |

## Workflow

1. **Parse URL**
   - Extract file key from URL
   - Extract node ID if present (`?node-id=X:Y`)
   - Pattern: `figma.com/(design|file)/([a-zA-Z0-9]+)`

2. **Validate MCP**
   - Check if Figma MCP tools available
   - If not: return error with setup instructions

3. **Extract via MCP**
   - Call Figma MCP with file key
   - If node ID: filter to specific node
   - Apply timeout (default 30s) - abort if exceeded
   - Limit component depth (default 5 levels)
   - Handle rate limit errors gracefully

4. **Transform Response**
   Extract and structure:
   - **Colors**: fills, strokes -> hex/rgba table
   - **Typography**: text nodes -> font/size/weight table
   - **Spacing**: auto-layout -> padding/gap table
   - **Components**: node tree -> hierarchy text

5. **Format Output**
   - markdown: Tables matching design-spec template Section 7
   - json: Structured object for programmatic use

6. **Return Result**
   - Save extraction output to `team-artifacts/designs/{YYMMDD}-figma-extract-{feature}.md`
   - Success: formatted specs
   - Partial: specs with warnings about missing data
   - Failed: error message with fallback suggestion

## URL Format
```
https://www.figma.com/design/{fileKey}/{fileName}?node-id={nodeId}
```

## Output Format (markdown)

### Colors
| Name    | Hex     | Usage          |
| ------- | ------- | -------------- |
| Primary | #3B82F6 | Buttons, links |

### Typography
| Element | Font  | Size | Weight |
| ------- | ----- | ---- | ------ |
| Heading | Inter | 24px | 600    |

### Spacing
| Element | Padding | Gap  |
| ------- | ------- | ---- |
| Card    | 16px    | 12px |

### Component Hierarchy
```
Frame "Card"
+-- Image "avatar"
+-- Text "name"
+-- Frame "actions"
    +-- Button "edit"
    +-- Button "delete"
```

## Error Handling

| Error            | Message                                                                                   |
| ---------------- | ----------------------------------------------------------------------------------------- |
| **No MCP**       | "Figma MCP not configured. See .claude/docs/figma-setup.md"                               |
| **Invalid URL**  | "Could not parse Figma URL. Expected: figma.com/design/{key}"                             |
| **Timeout**      | "Figma extraction timed out after {timeout}s. Try with specific node-id or reduce depth." |
| **Rate limited** | "Figma API rate limit reached. Try again later."                                          |
| **Not found**    | "Figma file not found or not accessible with current token"                               |
| **Too deep**     | "Component hierarchy exceeds max depth ({depth}). Results truncated."                     |

## Configuration Defaults

| Setting             | Value      | Rationale                 |
| ------------------- | ---------- | ------------------------- |
| Max Component Depth | 5 levels   | Prevents token bloat      |
| Extraction Timeout  | 30 seconds | Prevents blocking         |
| Max Colors          | 20         | Focus on primary palette  |
| Max Typography      | 10         | Focus on main text styles |

## Example

```bash
/figma-extract https://www.figma.com/design/ABC123/MyDesign?node-id=1:2
```

## Related
- **Role Skill:** `ux-designer`
- **Used by:** `/design-spec`
- **MCP:** Requires figma MCP tools

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
