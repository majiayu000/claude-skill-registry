---
name: figma-designer
description: Analyzes Figma designs and generates implementation-ready PRDs with detailed visual specifications. Use when user provides Figma link or uploads design screenshots. Requires Figma MCP server connection.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebFetch, WebSearch, AskUserQuestion
hooks:
  after_complete:
    - trigger: prd-planner
      mode: ask_first
      condition: prd_generated
      reason: "Further refine PRD with 4-file pattern"
    - trigger: self-improving-agent
      mode: background
      reason: "Learn design patterns for future reference"
    - trigger: session-logger
      mode: auto
      reason: "Save design analysis session"
---

# Figma Designer

> "Transform Figma designs into implementation-ready specifications with pixel-perfect accuracy"

## Overview

This skill analyzes Figma designs through the Figma MCP server and generates detailed PRDs with precise visual specifications. It extracts design tokens, component specifications, and layout information that developers can implement directly.

## Prerequisites

### Figma MCP Server

Ensure the Figma MCP server is connected and accessible:

```bash
# Check if Figma MCP is available
mcp-list
```

If not available, install from: https://github.com/modelcontextprotocol/servers

Required Figma MCP tools:
- `figma_get_file` - Get file metadata
- `figma_get_nodes` - Get node details
- `figma_get_components` - Get component information

## When This Skill Activates

Activates when you:
- Provide a Figma link (`https://www.figma.com/file/...`)
- Upload a design screenshot and mention "Figma"
- Say "analyze this design" or "extract design specs"
- Ask to "create PRD from Figma"

## Design Analysis Workflow

### Phase 1: Fetch Design Data

```yaml
Input: Figma URL or File Key
  ↓
Extract File Key from URL
  ↓
Call figma_get_file to get metadata
  ↓
Call figma_get_nodes to get design tree
  ↓
Parse frame, component, and text nodes
```

### Phase 2: Extract Design Tokens

Create a comprehensive design token inventory:

```typescript
// Design Token Structure
interface DesignTokens {
  colors: {
    primary: string[];
    secondary: string[];
    neutral: string[];
    semantic: {
      success: string;
      warning: string;
      error: string;
      info: string;
    };
  };
  typography: {
    fontFamilies: Record<string, string>;
    fontSizes: Record<string, number>;
    fontWeights: Record<string, number>;
    lineHeights: Record<string, number>;
    letterSpacing: Record<string, number>;
  };
  spacing: {
    scale: number;  // 4, 8, 12, 16, etc.
    values: Record<string, number>;
  };
  borders: {
    radii: Record<string, number>;
    widths: Record<string, number>;
  };
  shadows: Array<{
    name: string;
    values: string[];
  }>;
}
```

### Phase 3: Analyze Component Hierarchy

```
File
├── Frames (Pages/Screens)
│   ├── Component Instances
│   │   ├── Primary Button
│   │   ├── Input Field
│   │   └── Card
│   └── Text Layers
│       ├── Headings
│       ├── Body
│       └── Labels
```

For each component, extract:
- **Props**: Size, variant, state
- **Layout**: Flex direction, alignment, gap, padding
- **Styles**: Fill, stroke, effects
- **Content**: Text content, icons, images
- **Constraints**: Responsive behavior

### Phase 4: Generate Visual Specifications

Use this template for each screen:

```markdown
## Screen: [Screen Name]

### Layout Structure

```
┌─────────────────────────────────────────┐
│ [Header/Nav]                              │
├─────────────────────────────────────────┤
│                                         │
│  [Main Content]                          │
│  ┌───────────┐  ┌───────────┐         │
│  │  Card 1   │  │  Card 2   │         │
│  └───────────┘  └───────────┘         │
│                                         │
├─────────────────────────────────────────┤
│ [Footer]                                 │
└─────────────────────────────────────────┘
```

### Design Specifications

#### Colors

| Token | Value | Usage |
|-------|-------|-------|
| Primary | `#007AFF` | Primary buttons, links |
| Background | `#FFFFFF` | Screen background |
| Surface | `#F5F5F7` | Cards, sections |
| Text Primary | `#1C1C1E` | Headings, body |
| Text Secondary | `#8E8E93` | Captions, labels |

#### Typography

| Style | Font | Size | Weight | Line Height | Letter Spacing |
|-------|------|------|--------|------------|---------------|
| Display Large | SF Pro Display | 28px | Bold (700) | 34px | -0.5px |
| Heading 1 | SF Pro Display | 24px | Bold (700) | 32px | -0.3px |
| Heading 2 | SF Pro Display | 20px | Semibold (600) | 28px | -0.2px |
| Body Large | SF Pro Text | 17px | Regular (400) | 24px | -0.4px |
| Body | SF Pro Text | 15px | Regular (400) | 22px | -0.3px |
| Caption | SF Pro Text | 13px | Regular (400) | 18px | -0.1px |

#### Spacing

| Token | Value | Usage |
|-------|-------|-------|
| xs | 4px | Icon padding |
| sm | 8px | Tight spacing |
| md | 12px | Card padding |
| lg | 16px | Section spacing |
| xl | 24px | Large gaps |
| 2xl | 32px | Page margins |

#### Component: Primary Button

```typescript
interface PrimaryButtonProps {
  size?: 'small' | 'medium' | 'large';
  variant?: 'primary' | 'secondary' | 'tertiary';
  disabled?: boolean;
}

// Sizes
size.small = {
  height: 32px,
  paddingHorizontal: 12px,
  fontSize: 15,
  iconSize: 16,
}

size.medium = {
  height: 40px,
  paddingHorizontal: 16px,
  fontSize: 15,
  iconSize: 20,
}

size.large = {
  height: 48px,
  paddingHorizontal: 24px,
  fontSize: 17,
  iconSize: 24,
}

// Variants
variant.primary = {
  backgroundColor: '#007AFF',
  color: '#FFFFFF',
}

variant.secondary = {
  backgroundColor: '#F5F5F7',
  color: '#007AFF',
}

variant.tertiary = {
  backgroundColor: 'transparent',
  color: '#007AFF',
}
```

#### Constraints & Responsive Behavior

| Element | Constraints | Responsive Behavior |
|---------|-------------|---------------------|
| Header | Left, Right, Top | Sticky on scroll |
| Sidebar | Left, Top, Bottom | Collapses to drawer on mobile |
| Content | Left, Right (16px) | Full width on mobile |

### Interaction States

| Element | Default | Hover | Pressed | Disabled |
|---------|---------|-------|--------|----------|
| Primary Button | opacity: 1 | opacity: 0.8 | opacity: 0.6 | opacity: 0.4 |
| Icon Button | opacity: 1 | background: rgba(0,0,0,0.05) | background: rgba(0,0,0,0.1) | opacity: 0.3 |
| Card | shadow: sm | shadow: md | - | opacity: 0.6 |
```

## Output Formats

### Option 1: Full PRD (Recommended)

Generates a complete 4-file PRD:
- `docs/{feature}-notes.md` - Design decisions
- `docs/{feature}-task-plan.md` - Implementation tasks
- `docs/{feature}-prd.md` - Product requirements
- `docs/{feature}-tech.md` - Technical specifications

### Option 2: Visual Spec Document

Generates a design specification document:
```
docs/{feature}-design-spec.md
```

### Option 3: Component Library

For design systems, generates:
```
src/components/
├── Button/
│   ├── Button.tsx
│   ├── Button.test.tsx
│   └── Button.stories.tsx
├── Input/
├── Card/
└── tokens.ts
```

## Quick Reference: Design Token Categories

### Always Extract These

| Category | What to Extract | Why |
|----------|----------------|-----|
| **Colors** | Hex/RGBA values | Theme consistency |
| **Typography** | Font family, size, weight, spacing | Text hierarchy |
| **Spacing** | Padding, margin, gap values | Layout alignment |
| **Borders** | Radius, width values | Shape consistency |
| **Shadows** | Offset, blur, spread, color | Depth perception |
| **Icons** | Name, size, color | Visual consistency |
| **Images** | URL, dimensions, fit mode | Asset management |

## Design Review Checklist

Before generating PRD, verify:

- [ ] All screens are accounted for
- [ ] Design tokens are extracted
- [ ] Component variants are documented
- [ ] Responsive behavior is specified
- [ ] Interaction states are defined
- [ ] Accessibility (WCAG) is considered
  - [ ] Color contrast ratio ≥ 4.5:1
  - [ ] Touch targets ≥ 44x44px
  - [ ] Focus indicators visible

## Frame Analysis Template

For each frame/screen in the Figma file:

```markdown
## Frame: {Frame Name}

### Purpose
{What this screen does}

### Elements

| Element | Type | Styles | Props |
|---------|------|--------|-------|
| {Name} | {Component/Text/Vector} | {css} | {props} |
| {Name} | {Component/Text/Vector} | {css} | {props} |

### Layout
- Container: {width, height, fill}
- Position: {absolute/relative}
- Constraints: {left, right, top, bottom}
- Auto Layout: {direction, spacing, padding, alignment}

### Content Hierarchy
1. {Primary element}
2. {Secondary element}
3. {Tertiary element}

### Notes
{Any special considerations}
```

## Integration with Other Skills

### Typical Workflow

```
Figma URL → figma-designer → Visual Specs
                                ↓
                           prd-planner → PRD
                                ↓
                           implementation → Code
                                ↓
                           code-reviewer → Quality Check
```

### Handoff to Development

After generating specifications:

```markdown
## Developer Handoff

### Design Files
- Figma: {url}
- Design Spec: {link}

### Design Tokens
- Generated: `tokens.ts`
- Color palette: `colors.ts`
- Typography: `typography.ts`

### Component Library
- Storybook: {url}
- Component docs: {link}

### Assets
- Icons: {folder}
- Images: {folder}
- Exports: {format}
```

## Best Practices

### DO

✅ Extract exact pixel values for critical dimensions
✅ Document component variants and states
✅ Include responsive breakpoints
✅ Note any platform differences (iOS vs Android)
✅ Include accessibility considerations
✅ Export design tokens as constants

### DON'T

❌ Round spacing values (use exact 4px/8px/12px)
❌ Ignore hover/focus states
❌ Skip constraint behavior
❌ Forget about empty states
❌ Omit loading states
❌ Assume platform defaults without verification

## Examples and Platform Notes

See `references/example-output.md` for a full sample output and platform-specific considerations.
