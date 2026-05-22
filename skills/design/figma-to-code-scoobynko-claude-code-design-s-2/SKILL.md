---
name: figma-to-code
description: Generate production-ready React/Next.js code from Figma designs. Instructs proper Figma MCP tool usage, component reuse strategies, and variant mapping. **CRITICAL: ALWAYS use this skill when user provides a Figma link or mentions implementing/redesigning from Figma design.** Never attempt manual implementation without invoking this skill first.
---

# Figma to Code Generator

## Purpose

Generate production-ready React/Next.js code from Figma designs. Provides systematic workflows for using Figma MCP tools, enforces component reuse, maps Figma variants to code props.

## When to Use

Use this skill when:
- User provides a Figma link to implement as code
- Creating a new page from Figma design
- Redesigning an existing page based on updated Figma designs
- Implementing a new component or component variant from Figma

Do not use this skill when:
- No Figma design is provided (user describes requirements verbally)
- Working on backend or non-UI code
- Making minor text or content updates to existing pages

## Prerequisites

**Required dependency:** Figma MCP Server must be installed.

**Before using Figma MCP tools**, verify the server is available by attempting to use any Figma MCP tool (e.g., `mcp__figma-desktop__get_metadata`). If you receive an error indicating the tool is not available:

**Prompt user with:**
```
❌ Figma MCP Server Not Installed

To use Figma designs with Claude Code, you need to install the Figma MCP server.

Installation steps:
1. Open Figma Desktop app
2. Navigate to the MCP server installation guide:
   https://developers.figma.com/docs/figma-mcp-server

3. Follow the installation instructions for your operating system

4. Restart Claude Code after installation

Also ensure:
- Figma Desktop app is running
- You're logged into Figma
- The design file is open or you have access to it
```

**Only proceed with Figma MCP tools after confirming the server is installed.**

## Figma MCP Tool Usage Protocol (MANDATORY)

### Critical Rule: ALWAYS Use This Workflow When User Provides Figma Link

When user provides a Figma link or node ID, **YOU MUST follow this exact tool sequence**. Do NOT skip steps or change the order.

### Required Tool Order: Metadata → Context → Screenshot → Variables

#### Step 1: Get Metadata (REQUIRED FIRST)
```
Tool: mcp__figma-desktop__get_metadata
Extract:
- Component/frame names and hierarchy
- Layer types (COMPONENT, FRAME, INSTANCE)
- Variant property names
- Child element structure
```

**Look for:** Component or frame? Variant properties? Children organization? Naming patterns?

#### Step 2: Get Design Context (REQUIRED SECOND)
```
Tool: mcp__figma-desktop__get_design_context
Extract:
- Colors (with variable references like "colors/iris/950")
- Spacing (padding, gaps, margins)
- Typography (font family, size, weight)
- Border radius, shadows, effects
- Component variant values
```

**Look for:** Which Figma variables? Spacing values? Hard-coded values?

#### Step 3: Get Screenshot (REQUIRED THIRD)
```
Tool: mcp__figma-desktop__get_screenshot
Use for: Visual verification, understanding layout
```

#### Step 4: Get Variables (REQUIRED FOURTH)
```
Tool: mcp__figma-desktop__get_variable_defs
When: Design uses Figma variables extensively or checking token consistency
```

### MCP Tool Parameters

Always include for proper logging:
```typescript
{ clientLanguages: "typescript,javascript", clientFrameworks: "react,nextjs" }
```

### MCP Tool Rules

**Do:** ✓ Start with metadata, ✓ Use context for details, ✓ Use parameters
**Don't:** ✗ Skip metadata, ✗ Wrong order, ✗ Screenshot alone

## Critical Boundaries: Frontend Layer Focus

### Default Scope: Frontend Only

Operate **exclusively in the frontend layer** by default. Figma designs represent UI/UX and should translate to frontend code only.

**Frontend scope:**
- `[FRONTEND_DIR]/app/` - Next.js pages and routes
- `[FRONTEND_DIR]/components/` - React components
- `[FRONTEND_DIR]/lib/` - Frontend utilities
- `[FRONTEND_DIR]/hooks/` - Custom React hooks
- `[FRONTEND_DIR]/public/` - Static assets

**Do NOT touch without permission:**
- `[BACKEND_DIR]/` - Backend directories and files
- Backend routes, database schemas, or API endpoints

### Backend Change Protocol

**ALWAYS ask user before:**
1. Creating new API routes
2. Modifying existing API endpoints
3. Changing database schemas
4. Adding backend dependencies
5. Touching any files outside [FRONTEND_DIR]/

**Ask with this format:**
```
⚠️ Backend Change Required

To implement this Figma design, the following backend changes are needed:
[Specific backend changes listed]

Frontend can be mocked with placeholder data until backend is ready.

Would you like me to:
1. Implement frontend with mocked data (recommended)
2. Implement both frontend and backend
3. Only implement frontend and document backend requirements
```

**Only proceed WITHOUT asking if:**
- User explicitly stated "implement both frontend and backend"
- User is actively working in backend and asks to "complete the implementation"

### Mock Data Pattern

Implement frontend with mock data first, document required API shape.

```tsx
// TODO: Replace with actual API call to [BACKEND_DIR]/[API_MODULE]
const mockProducts = [{ id: 1, name: "Product 1", price: 99 }]

/**
 * Backend API Required:
 * GET /api/products
 * Response: { products: Array<{id, name, price, imageUrl}> }
 * Backend file: [BACKEND_DIR]/[API_MODULE]/routes.ts
 */
export function ProductList() {
  const products = mockProducts
  return // Render using mock data
}
```

## Component Reuse Strategy

### Priority: Reuse > Extend > Create

#### Check Existing Components First

**Search locations:**
- `[COMPONENTS_DIR]/ui/` - UI library base components
- `[COMPONENTS_DIR]/` - Custom components

**Search method:**
1. Extract base name from Figma (e.g., "Button" from "Button/Primary/Large")
2. Use Glob to find: `[COMPONENTS_DIR]/ui/{name}.tsx`
3. Read component file to check variants and props
4. Compare Figma variants with code props

**Key components to check for:**
- Button, Card, Dialog, Form, Input, Select, Textarea, Checkbox, Switch
- Alert, Badge, Tabs, Accordion, Table, DropdownMenu, Popover, Tooltip
- Other custom components in your UI library

#### Decision Matrix

| Figma Design | Action |
|-------------|--------|
| Matches existing exactly | Use existing with props |
| Matches with minor tweaks | Use existing + className |
| Can be composed | Use composition pattern |
| Needs new variant | **Ask user** before extending |
| Completely new pattern | Create new component |

## Variant Mapping: Figma → Code

### Common Mappings

| Figma Property | Figma Value | Code Prop | Code Value |
|---------------|-------------|-----------|------------|
| variant | Primary | variant | "primary" |
| variant | Secondary | variant | "secondary" |
| variant | Outlined | variant | "outline" |
| size | Small | size | "sm" |
| size | Large | size | "lg" |
| state | Disabled | disabled | true |

### Multiple Variants Example

```tsx
// Figma: Button/Primary/Large/Disabled
<Button variant="primary" size="lg" disabled={true}>Text</Button>
```

### Creating New Components with Variants

```tsx
// Example: Using your styling system for variants
const componentVariants = [VARIANT_SYSTEM_IMPLEMENTATION]
// Map Figma variant properties to your component's variant props
// e.g., Figma "Primary" -> variant="primary"
// e.g., Figma "Small" -> size="sm"
```

## Code Generation Guidelines

### TypeScript Component Pattern

```tsx
import * as React from "react"
import { [STYLING_UTILITY] } from "[UTILITY_PATH]"

interface ComponentNameProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "primary" | "secondary"  // Map from Figma variants
  size?: "sm" | "lg"  // Map from Figma size variants
}

export const ComponentName = React.forwardRef<HTMLDivElement, ComponentNameProps>(
  ({ className, variant = "primary", size = "lg", ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={[APPLY_STYLES_BASED_ON_VARIANTS]}
        {...props}
      />
    )
  }
)

ComponentName.displayName = "ComponentName"
```

### Styling Priority

1. **Design System Variables** (preferred): Use your project's semantic design tokens
2. **Custom Palette**: Use your project's defined color palette
3. **Never:** Hard-coded color values or arbitrary styles

**Map Figma colors to your design system:**
- Extract color variable names from Figma design context
- Map to your project's color system (CSS variables, theme tokens, etc.)
- Example: `colors/primary/600` → `[YOUR_PRIMARY_COLOR_TOKEN]`

### Responsive & Dark Mode

```tsx
// Use your project's responsive breakpoint system
className={[RESPONSIVE_LAYOUT_CLASSES]}

// Use your project's theme/dark mode system
className={[THEME_AWARE_CLASSES]}
```

## Coding Standards

### File Naming and Location

**Naming:**
- Components: PascalCase (`ProductCard.tsx`)
- Utilities: kebab-case (`format-date.ts`)
- Pages: Next.js convention (`page.tsx`)

**Locations:**
- UI components: `[COMPONENTS_DIR]/ui/component-name.tsx`
- Feature components: `[COMPONENTS_DIR]/feature-name/component-name.tsx`
- Page components: `[PAGES_DIR]/route/component-name.tsx`

### TypeScript & Code Style

- **TypeScript**: No `any` types, proper interfaces
- **Immutability**: Use `const` and `readonly`
- **Null handling**: Prefer `null` over `undefined`
- **Functional patterns**: No classes
- **Styling**: Follow your project's styling approach (no inline styles unless project convention allows)
- **Descriptive names**: `isLoading`, `hasError`
- One component per file
- Place tests next to components

**Import order:**
```tsx
// 1. React/frameworks
import * as React from "react"
// 2. External packages
import { [EXTERNAL_UTILITIES] } from "[PACKAGE]"
// 3. Internal components
import { Button } from "[COMPONENTS_DIR]/ui/button"
// 4. Types
import type { User } from "[TYPES_DIR]"
```

## Accessibility Requirements

Always include:
- **Semantic HTML**: `<button>`, `<nav>`, `<main>`
- **ARIA labels**: When semantic HTML isn't enough
- **Keyboard navigation**: Focus states, tab order
- **Screen reader support**: alt text, aria-labels

```tsx
<button aria-label="Close" aria-pressed={isActive} disabled={isDisabled}>
  <X className="h-4 w-4" aria-hidden="true" />
</button>
```

## Page Generation

### Creating Full Pages

1. Get metadata to understand sections
2. Get context for each section
3. Identify which map to existing components
4. Generate using composition

```tsx
// [PAGES_DIR]/route-name/page.tsx
import { ComponentA } from "[COMPONENTS_DIR]/ui/component-a"

export default function PageName() {
  return (
    <div className={[CONTAINER_STYLES]}>
      <header><h1 className={[HEADING_STYLES]}>Page Title</h1></header>
      <main className={[LAYOUT_STYLES]}><ComponentA /></main>
    </div>
  )
}
```

### Redesigning Pages

1. Read current page first
2. Identify changes vs. staying same
3. Preserve data fetching and state
4. Update only UI layer
5. Ask before removing functionality

## Quality Checklist

Before providing code, verify:

- [ ] Used metadata → context → screenshot → variables order
- [ ] Checked for existing components first
- [ ] Used composition over creation
- [ ] Mapped Figma variants to code props
- [ ] Used project's design system tokens/variables
- [ ] No `any` types, proper TypeScript
- [ ] Included accessibility attributes
- [ ] Responsive design following project conventions
- [ ] Theme/dark mode support if applicable
- [ ] Correct file naming and location
- [ ] Added component displayName
- [ ] JSDoc comments for complex logic
- [ ] **All code in frontend directory only**
- [ ] **No backend changes without permission**
- [ ] **Used mock data if backend needed**

## Examples

For detailed workflow examples, see the reference file: `examples.md`

Examples include:
- Button component reuse
- Card composition
- Page with backend requirements
- Creating new component with variants
- Full page layout implementation
- Common patterns (composition, extending, mock data)

## Error Handling

**When Figma data unclear:** Ask for clarification, use screenshot as fallback, document assumptions

**When no component matches:** Document why existing don't work, ask user: extend or create new?

**When backend requirements unclear:** Document API shape in JSDoc, use TypeScript interfaces, provide mock data
