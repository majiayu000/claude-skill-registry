---
name: stitch-to-react
description: Converts Google Stitch exports into React components with design DNA integration. Use when user references design-intent/google-stitch exports, mentions "convert Stitch output", "Stitch to React", or processes Stitch code directories containing HTML + PNG pairs.
argument-hint: "[stitch-directory]"
---

# Stitch to React

Convert Google Stitch exports (Tailwind HTML + PNG) into React components with full design system integration.

**Core Philosophy**: Decompose Stitch screens into composable React components while respecting established patterns.

## Quick Start

### 0. Verify Exports Exist (Mandatory)

Before any conversion, verify Stitch exports are available:

```bash
# Check for HTML/PNG pairs in the expected location
Glob: design-intent/google-stitch/{feature}/exports/*.html
Glob: design-intent/google-stitch/{feature}/exports/*.png
```

**If exports found:** Proceed to Step 1.

**If exports NOT found:**
1. Check if user specified wrong path - ask for correct location
2. Suggest running `/stitch-generate` first to create exports
3. Fall back to design docs: Check `/design-intent/patterns/` for established patterns or project directories for screenshots
4. If no design assets exist, inform user and offer to help create them

**Report findings:**
```
Export Check: [PASSED/MISSING]
- HTML files: [count] found
- PNG files: [count] found
- Location: design-intent/google-stitch/{feature}/exports/
```

### 1. Load Project Context (Mandatory)

Before any conversion:

1. Read `/design-intent/memory/constitution.md` for project principles
2. Read `/design-intent/patterns/` for established patterns
3. Detect project design system (Fluent UI, Material UI, custom, etc.)
4. Report: "Existing patterns to consider: [list]"

### 2. Scan Stitch Exports

Stitch exports are located at:
```
design-intent/google-stitch/{feature}/exports/
├── 01-layout-{name}.html    # Tailwind CSS + HTML
├── 01-layout-{name}.png     # Visual reference
├── 02-component-{name}.html
├── 02-component-{name}.png
└── ...
```

From each HTML file, extract:
- Inline `tailwind.config` (colors, fonts, spacing)
- Custom `<style>` blocks (animations, keyframes)
- DOM structure for component hierarchy
- Material Symbols icons usage

### 3. Map to Project Design System

For each Stitch element:

1. **Check existing patterns** - Can we reuse established components?
2. **Map Tailwind tokens** - Convert to project design tokens
3. **Decompose into composable parts** - Break screens into smaller, reusable components
4. **Flag conflicts** - Note when Stitch output differs from patterns

### 4. Generate React Components

Output structure:
```
src/components/{feature}/
├── {ComponentName}.tsx     # Main component
├── {SubComponent}.tsx      # Decomposed smaller components
├── tokens.ts               # Design tokens from Stitch config
├── types.ts                # TypeScript interfaces
└── index.ts                # Re-exports
```

## Component Selection Priority

Per constitution principles:

1. **Existing project components** from `/design-intent/patterns/`
2. **Framework components** (Fluent UI, project design system)
3. **Custom components** (document with header comment)

## Conflict Resolution

When Stitch output conflicts with patterns:

```
## Design Conflict Detected

**Element**: Button border-radius
**Stitch Output**: 4px
**Existing Pattern**: 8px (button-styling.md)

### Options
1. Follow Stitch output - Use 4px
2. Use existing pattern - Use 8px
3. Update pattern - Make 4px the new standard

Which approach?
```

## Custom Component Documentation

```tsx
/**
 * CUSTOM COMPONENT: ComponentName
 * Source: Stitch screen name
 * Base: @fluentui/react-components/ComponentType (if applicable)
 * Reason: Why custom implementation was needed
 * Created: YYYY-MM-DD
 *
 * Original Reference: design-intent/google-stitch/{feature}/exports/{screen}.png
 */
```

## Reference Documentation

- **Detailed workflow**: See [WORKFLOW.md](WORKFLOW.md)
- **Usage examples**: See [EXAMPLES.md](EXAMPLES.md)
- **Common issues**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

## Invocation

Triggered by:

- User references `design-intent/google-stitch/` exports
- "Convert Stitch output to React"
- "Stitch to React" requests
- Processing directories with HTML + PNG pairs from Stitch
