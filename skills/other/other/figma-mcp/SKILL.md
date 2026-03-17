---
name: figma-mcp
description: Convert Figma designs into production-ready code using MCP server tools. Use this skill when users provide Figma URLs, request design-to-code conversion, ask to implement Figma mockups, or need to extract design tokens and system values from Figma files. Works with frames, components, and entire design files to generate HTML, CSS, React, or other frontend code.
---

# Figma MCP

## Overview

This skill enables accurate design-to-code conversion by leveraging Figma's MCP (Model Context Protocol) server to access structured design data directly from Figma files. Unlike screenshot-based approaches, the Figma MCP provides semantic information about every design element including exact spacing, colors, typography, component hierarchy, and design system tokens, resulting in significantly more accurate code generation.

## When to Use This Skill

Trigger this skill when users:
- Provide Figma URLs (file links or frame selection links)
- Request converting/implementing Figma designs into code
- Ask to "build this from Figma" or "implement this design"
- Need to extract design tokens, variables, or design system values
- Want to update existing code to match a Figma design
- Mention maintaining design-to-code consistency

## Workflow

### Step 1: Receive Figma Design Reference

When a user provides a Figma URL or requests design implementation:

1. **Identify the Figma link type**:
   - File URL: `https://www.figma.com/file/[FILE_KEY]/...`
   - Frame selection: `https://www.figma.com/file/[FILE_KEY]/...?node-id=[NODE_ID]`
   - Design URL: `https://www.figma.com/design/[FILE_KEY]/...`

2. **Confirm access**:
   - Verify the Figma MCP server is configured and accessible
   - If not configured, reference `references/setup-guide.md` for setup instructions

### Step 2: Fetch Design Data Using MCP Tools

Use the available Figma MCP tools to retrieve structured design data:

**Key MCP Tools Available:**
- **get_figma_data** - Fetch complete design data for a file or specific frame
- **get_figma_variables** - Extract design tokens (colors, spacing, typography)
- **get_figma_components** - Retrieve component definitions and instances
- **get_figma_styles** - Access text, color, and effect styles

**Best Practice:** Start with `get_figma_data` for the specific frame or node the user referenced. This provides the complete structure, layout data, and styling information.

**Example workflow:**
```
User: "Implement this Figma design: [Figma URL with node-id]"

1. Extract file_key and node_id from URL
2. Call get_figma_data with file_key and node_id parameters
3. Receive structured JSON with:
   - Element hierarchy (frames, groups, components)
   - Layout properties (position, size, constraints, auto-layout)
   - Styling (fills, strokes, effects, typography)
   - Component instances and variants
   - Design tokens and variables
```

### Step 3: Analyze Design Structure

Before generating code, analyze the fetched design data:

1. **Identify component hierarchy**:
   - What are the main containers/sections?
   - Which elements are reusable components?
   - How does the layout flow (flex, grid, absolute)?

2. **Extract design system values**:
   - Colors (fills, strokes, backgrounds)
   - Typography (font families, sizes, weights, line heights)
   - Spacing (padding, margins, gaps)
   - Borders, shadows, effects

3. **Determine layout approach**:
   - Auto-layout frames → Flexbox or CSS Grid
   - Absolute positioning → CSS absolute/relative positioning
   - Constraints → Responsive behavior

### Step 4: Generate Code

Generate production-ready code based on the design data:

**Code generation principles:**

1. **Use semantic HTML**:
   - Frames → `<div>`, `<section>`, `<header>`, etc.
   - Text → `<h1>-<h6>`, `<p>`, `<span>`
   - Buttons → `<button>`
   - Images → `<img>`

2. **Preserve design system values**:
   - Extract color variables from Figma variables
   - Create CSS custom properties for spacing, colors, typography
   - Use exact values from design (don't approximate)

3. **Match layout behavior**:
   - Auto-layout with padding/gap → Flexbox with gap/padding
   - Auto-layout direction → flex-direction
   - Constraints → Responsive CSS (flex-grow, min/max-width)

4. **Component-based architecture**:
   - Figma components → React/Vue components or CSS classes
   - Component instances → Component usage with props
   - Variants → Props or conditional classes

5. **Responsive considerations**:
   - Use relative units where appropriate (rem, em, %)
   - Consider breakpoints for desktop/mobile variants
   - Preserve constraint behavior from Figma

**Example output structure:**
```typescript
// For React
import React from 'react';
import './styles.css';

export const ComponentName = () => {
  return (
    <div className="container">
      {/* Preserved hierarchy and styling */}
    </div>
  );
};
```

### Step 5: Validate and Refine

After generating initial code:

1. **Verify accuracy**:
   - Do spacing values match the design exactly?
   - Are colors accurate (check hex values)?
   - Does the layout behavior match (responsive, wrapping)?

2. **Check for improvements**:
   - Can any values be extracted to CSS variables?
   - Are there repeated patterns that should be componentized?
   - Is the code accessible (semantic HTML, ARIA attributes)?

3. **Offer refinements**:
   - Suggest design system integration if applicable
   - Mention any design inconsistencies detected
   - Propose optimizations (shared styles, component extraction)

## Best Practices

### Design-to-Code Accuracy

- **Never approximate values**: Use exact pixel values, colors, and measurements from Figma data
- **Preserve hierarchy**: Maintain the nesting structure from Figma frames/groups
- **Match auto-layout behavior**: Figma's auto-layout maps directly to Flexbox properties
- **Use design tokens**: Extract and reuse color/spacing variables from Figma Variables

### Code Quality

- **Semantic HTML**: Use appropriate HTML elements, not just divs
- **Component extraction**: Identify reusable components from Figma components
- **CSS organization**: Separate layout, typography, and visual styling
- **Accessibility**: Add appropriate ARIA labels and semantic structure

### Design System Integration

- **Check for variables**: Use Figma Variables for design tokens
- **Component consistency**: Match Figma component names to code component names
- **Code Connect**: If available, reference Code Connect mappings for components
- **Naming conventions**: Follow existing project conventions for classes/components

### Performance

- **Optimize images**: Suggest appropriate image formats and compression
- **CSS efficiency**: Avoid redundant styles, use CSS variables
- **Bundle size**: Keep generated code lean and modular

For more detailed guidance, reference:
- `references/setup-guide.md` - Setting up Figma MCP server
- `references/best-practices.md` - Extended best practices and examples

## Common Patterns

### Pattern 1: Landing Page from Figma
```
User provides: Figma link to landing page design
Process:
1. Fetch complete page structure with get_figma_data
2. Identify sections (hero, features, CTA, footer)
3. Generate semantic HTML with section elements
4. Extract colors/typography to CSS variables
5. Implement responsive behavior from constraints
```

### Pattern 2: Component Implementation
```
User provides: Figma link to button component with variants
Process:
1. Fetch component definition with get_figma_components
2. Identify variants (primary, secondary, sizes)
3. Create React component with props for variants
4. Extract shared styles to base component
5. Implement variant-specific styles as props/classes
```

### Pattern 3: Design System Extraction
```
User requests: Extract design tokens from Figma file
Process:
1. Fetch variables with get_figma_variables
2. Fetch text/color styles with get_figma_styles
3. Generate CSS custom properties or theme object
4. Document token naming and usage
5. Export as stylesheet or config file
```

## Troubleshooting

**MCP server not available:**
- Check if Figma MCP server is configured in MCP settings
- Reference `references/setup-guide.md` for setup instructions
- Verify user has appropriate Figma plan (Dev Mode access for official server)

**Design data incomplete:**
- Ensure the Figma file is accessible (permissions)
- Verify the node-id in the URL is correct
- Try fetching parent frame if child node returns limited data

**Code doesn't match design visually:**
- Double-check spacing and sizing values
- Verify color values are exact hex codes from Figma
- Check if fonts are loaded correctly
- Review auto-layout direction and alignment properties

## Resources

This skill includes reference documentation to support Figma MCP workflows:

### references/setup-guide.md
Complete setup instructions for configuring Figma MCP server (official and community options) in Claude Code and other MCP clients. Reference when users need to set up the integration.

### references/best-practices.md
Extended best practices, detailed examples, and advanced patterns for design-to-code conversion including component architecture, responsive design strategies, and design system integration.
