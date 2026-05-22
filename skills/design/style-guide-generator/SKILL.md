---
description: Use this skill when the user asks to "generate a style guide", "create design system documentation", "document design tokens", "create a design system", "document colors and typography", mentions "design tokens", "component library documentation", or wants to create comprehensive design system documentation with Storybook. This skill provides guidance on organizing and documenting design systems, color palettes, typography scales, spacing systems, and component patterns.
---

# Style Guide Generator Skill

## Overview

Generate comprehensive design system documentation for Storybook, including design tokens (colors, typography, spacing), component guidelines, and usage patterns. Create a centralized source of truth for your design system.

This skill provides guidance on structuring design system documentation using Storybook's docs features (MDX, Doc Blocks) and organizing design tokens.

## What This Skill Provides

### Design System Documentation
Create comprehensive documentation for:
- **Design tokens**: Colors, typography, spacing, shadows, borders
- **Component guidelines**: Usage patterns, do's and don'ts
- **Brand guidelines**: Logo usage, voice and tone
- **Accessibility standards**: WCAG compliance, keyboard navigation
- **Code examples**: Implementation snippets

### Storybook Docs Integration
Use Storybook's documentation features:
- **MDX pages**: Rich documentation with interactive examples
- **Doc Blocks**: Pre-built components for common documentation patterns
- **Custom pages**: Design system landing page, getting started guides
- **Auto-generated docs**: Component API documentation

### Design Token Organization
Structure and document design tokens:
- **Color system**: Primary, secondary, semantic colors
- **Typography scale**: Font families, sizes, weights, line heights
- **Spacing scale**: Consistent spacing system (4px, 8px, 16px, etc.)
- **Elevation system**: Shadows and z-index
- **Border styles**: Radius, width, colors

### Component Documentation
Document component patterns:
- **Anatomy**: Component structure and parts
- **Variants**: Available options and use cases
- **States**: Hover, focus, active, disabled, loading
- **Accessibility**: ARIA attributes, keyboard support
- **Examples**: Real-world usage scenarios

## Design System Structure

### Recommended Storybook Organization

```
.storybook/
├── pages/
│   ├── Introduction.mdx          # Design system overview
│   ├── GettingStarted.mdx        # Installation and usage
│   ├── DesignPrinciples.mdx      # Design philosophy
│   ├── Accessibility.mdx         # A11y guidelines
│   └── Contributing.mdx          # Contribution guide
├── design-tokens/
│   ├── Colors.mdx                # Color palette docs
│   ├── Typography.mdx            # Typography scale
│   ├── Spacing.mdx               # Spacing system
│   ├── Elevation.mdx             # Shadows and depth
│   └── Borders.mdx               # Border styles
├── components/
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.stories.tsx
│   │   └── Button.mdx            # Component docs
│   ├── Input/
│   └── Card/
└── patterns/
    ├── Forms.mdx                  # Form patterns
    ├── Navigation.mdx             # Navigation patterns
    └── Layouts.mdx                # Layout patterns
```

## Creating MDX Documentation Pages

### Introduction Page

```mdx
# Welcome to Our Design System

A comprehensive collection of reusable components, design tokens, and guidelines
for building consistent user experiences.

## Quick Links

- [Getting Started](/docs/getting-started)
- [Design Tokens](/docs/design-tokens-colors)
- [Components](/docs/components)
- [Accessibility](/docs/accessibility)

## Design Principles

1. **Consistency**: Use established patterns across the product
2. **Accessibility**: WCAG 2.1 AA compliance by default
3. **Performance**: Optimized components for fast load times
4. **Flexibility**: Composable primitives for custom needs

## Installation

```bash
npm install @your-org/design-system
```

## Usage

```tsx
import { Button, Card } from '@your-org/design-system';

function App() {
  return (
    <Card>
      <Button variant="primary">Get Started</Button>
    </Card>
  );
}
```
```

### Color Documentation Page

```mdx
import { ColorPalette, ColorItem } from '@storybook/blocks';

# Colors

Our color system is designed for accessibility, consistency, and scalability.

## Primary Colors

<ColorPalette>
  <ColorItem
    title="Primary"
    subtitle="Brand color"
    colors={{
      'Primary 50': '#e3f2fd',
      'Primary 100': '#bbdefb',
      'Primary 500': '#2196f3',
      'Primary 900': '#0d47a1',
    }}
  />
</ColorPalette>

## Semantic Colors

<ColorPalette>
  <ColorItem
    title="Success"
    colors={{ Success: '#4caf50' }}
  />
  <ColorItem
    title="Warning"
    colors={{ Warning: '#ff9800' }}
  />
  <ColorItem
    title="Error"
    colors={{ Error: '#f44336' }}
  />
  <ColorItem
    title="Info"
    colors={{ Info: '#2196f3' }}
  />
</ColorPalette>

## Accessibility

All color combinations meet WCAG 2.1 AA standards:

- Text on Primary 500: White (#ffffff) - Contrast ratio 4.5:1 ✓
- Text on Primary 900: White (#ffffff) - Contrast ratio 8.2:1 ✓

## Usage

```tsx
// CSS
.primary-button {
  background-color: var(--color-primary-500);
  color: white;
}

// Tailwind
<button className="bg-primary-500 text-white">
  Click me
</button>
```
```

### Typography Documentation Page

```mdx
import { Typeset } from '@storybook/blocks';

# Typography

Our typography system ensures consistent, accessible text across all products.

## Font Families

- **Sans**: 'Inter', -apple-system, system-ui, sans-serif
- **Serif**: 'Merriweather', Georgia, serif
- **Mono**: 'Fira Code', Consolas, monospace

## Type Scale

<Typeset
  fontSizes={[12, 14, 16, 20, 24, 32, 40, 48]}
  fontWeight={400}
  sampleText="The quick brown fox jumps over the lazy dog"
  fontFamily="'Inter', sans-serif"
/>

## Heading Styles

| Element | Size | Weight | Line Height | Usage |
|---------|------|--------|-------------|-------|
| H1 | 48px | 700 | 1.2 | Page titles |
| H2 | 40px | 700 | 1.2 | Section headings |
| H3 | 32px | 600 | 1.3 | Subsection headings |
| H4 | 24px | 600 | 1.4 | Card titles |
| H5 | 20px | 600 | 1.5 | Small headings |
| H6 | 16px | 600 | 1.5 | Overlines |

## Body Text

| Style | Size | Weight | Line Height | Usage |
|-------|------|--------|-------------|-------|
| Large | 18px | 400 | 1.6 | Introductions |
| Regular | 16px | 400 | 1.5 | Body text |
| Small | 14px | 400 | 1.5 | Captions, labels |
| Tiny | 12px | 400 | 1.5 | Helper text |

## Usage

```tsx
// CSS
h1 {
  font-size: var(--font-size-h1);
  font-weight: var(--font-weight-bold);
  line-height: var(--line-height-tight);
}

// React
<Text variant="h1">Heading</Text>
<Text variant="body">Regular text</Text>
<Text variant="small">Small text</Text>
```
```

### Spacing Documentation Page

```mdx
# Spacing

Consistent spacing creates visual rhythm and hierarchy.

## Spacing Scale

Our spacing system uses a 4px base unit:

| Token | Value | Usage |
|-------|-------|-------|
| `space-0` | 0px | No spacing |
| `space-1` | 4px | Tight spacing |
| `space-2` | 8px | Small spacing |
| `space-3` | 12px | Medium-small |
| `space-4` | 16px | Regular spacing |
| `space-5` | 20px | Medium spacing |
| `space-6` | 24px | Large spacing |
| `space-8` | 32px | XL spacing |
| `space-10` | 40px | XXL spacing |
| `space-12` | 48px | Section spacing |
| `space-16` | 64px | Page spacing |

## Visual Example

<div style={{ display: 'flex', gap: '16px', alignItems: 'flex-start' }}>
  <div style={{ background: '#e3f2fd', height: '40px', width: '4px' }} />
  <span>space-1 (4px)</span>
</div>

<div style={{ display: 'flex', gap: '16px', alignItems: 'flex-start', marginTop: '8px' }}>
  <div style={{ background: '#e3f2fd', height: '40px', width: '16px' }} />
  <span>space-4 (16px)</span>
</div>

<div style={{ display: 'flex', gap: '16px', alignItems: 'flex-start', marginTop: '8px' }}>
  <div style={{ background: '#e3f2fd', height: '40px', width: '32px' }} />
  <span>space-8 (32px)</span>
</div>

## Usage Guidelines

### Component Spacing
- **Between elements**: Use space-4 (16px) as default
- **Component padding**: Use space-4 or space-6 (16px or 24px)
- **Section spacing**: Use space-12 or space-16 (48px or 64px)

### Grid and Layout
- **Column gap**: space-4 (16px) for tight, space-6 (24px) for loose
- **Row gap**: space-6 (24px) for cards, space-4 (16px) for lists

## Usage

```tsx
// CSS
.card {
  padding: var(--space-6);
  margin-bottom: var(--space-4);
}

// Tailwind
<div className="p-6 mb-4">Card content</div>

// Styled components
const Card = styled.div`
  padding: ${props => props.theme.space[6]};
`;
```
```

## Component Documentation Pattern

### Button Component Documentation

```mdx
import { Meta, Canvas, Story, Controls } from '@storybook/blocks';
import * as ButtonStories from './Button.stories';

<Meta of={ButtonStories} />

# Button

Primary UI component for user interactions. Use buttons for actions like submitting forms, opening dialogs, or navigating.

## When to Use

✅ **Use buttons when:**
- Triggering actions (submit, save, delete)
- Opening modals or dialogs
- Navigating to new pages
- Confirming decisions

❌ **Don't use buttons for:**
- Navigation within content (use links instead)
- Selecting from multiple options (use radio/checkbox)
- Showing/hiding content (use disclosure patterns)

## Examples

### Primary Button

The primary button is for the main action on a page.

<Canvas of={ButtonStories.Primary} />

### Secondary Button

Use secondary buttons for secondary actions.

<Canvas of={ButtonStories.Secondary} />

### All Variants

<Controls of={ButtonStories.Primary} />

## Variants

| Variant | Usage |
|---------|-------|
| Primary | Main action on page |
| Secondary | Secondary actions |
| Outline | Tertiary actions |
| Ghost | Subtle actions |

## Sizes

| Size | Usage |
|------|-------|
| Small | Compact UIs, tables |
| Medium | Default size |
| Large | Hero sections, CTAs |

## States

- **Default**: Normal interactive state
- **Hover**: Visual feedback on hover
- **Active**: Visual feedback on click
- **Focus**: Keyboard focus indicator
- **Disabled**: Non-interactive state
- **Loading**: Async action in progress

## Accessibility

✅ **Built-in features:**
- Semantic `<button>` element
- Keyboard accessible (Enter/Space)
- Focus visible indicator
- `aria-busy` when loading
- Disabled state prevents interaction

## Best Practices

1. **Use clear labels**: "Save changes" not "Submit"
2. **One primary button per page**: Avoid multiple CTAs
3. **Loading states**: Show feedback for async actions
4. **Icon buttons**: Include `aria-label`

## Code Example

```tsx
import { Button } from '@your-org/design-system';

function MyComponent() {
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    await saveData();
    setLoading(false);
  };

  return (
    <Button
      variant="primary"
      onClick={handleSubmit}
      loading={loading}
    >
      Save Changes
    </Button>
  );
}
```
```

## Storybook Configuration

### Configure Docs in `.storybook/main.ts`

```typescript
import type { StorybookConfig } from '@storybook/react-vite';

const config: StorybookConfig = {
  stories: [
    '../docs/**/*.mdx',
    '../src/**/*.stories.@(js|jsx|ts|tsx)',
  ],
  addons: [
    '@storybook/addon-links',
    '@storybook/addon-essentials',
    '@storybook/addon-docs',
  ],
  docs: {
    autodocs: true,
    defaultName: 'Documentation',
  },
};

export default config;
```

### Organize Sidebar in `.storybook/preview.ts`

```typescript
export const parameters = {
  options: {
    storySort: {
      order: [
        'Introduction',
        'Getting Started',
        'Design Tokens',
        ['Colors', 'Typography', 'Spacing', 'Elevation'],
        'Components',
        'Patterns',
      ],
    },
  },
};
```

## AI-Powered Visual Generation

Optionally integrate with the **visual-design** skill to generate visual assets:

```bash
# Generate color palette visualization
python3 ${CLAUDE_PLUGIN_ROOT}/skills/visual-design/scripts/generate_mockup.py \
  "Color palette for modern design system with primary blue, success green, error red" \
  --output style-guide/color-palette.png

# Generate typography scale
python3 ${CLAUDE_PLUGIN_ROOT}/skills/visual-design/scripts/generate_mockup.py \
  "Typography scale showing font sizes from 12px to 48px" \
  --output style-guide/typography.png
```

**Note:** Requires `OPENROUTER_API_KEY`. Gracefully skips if unavailable.

## Best Practices

### Documentation Structure
1. **Start with overview**: What is the design system?
2. **Show quick start**: Get developers using it fast
3. **Document tokens first**: Foundation before components
4. **Include examples**: Real code, not just descriptions
5. **Maintain guidelines**: Keep docs up to date

### Component Documentation
1. **Show, don't tell**: Use Canvas to demonstrate
2. **Provide guidance**: When to use, when not to use
3. **Document states**: Show all interactive states
4. **Include accessibility**: Built-in a11y features
5. **Add code examples**: Copy-paste ready snippets

### Design Token Documentation
1. **Visual representation**: Show colors, not just hex codes
2. **Usage guidelines**: When to use each token
3. **Accessibility notes**: Contrast ratios, readability
4. **Code examples**: How to apply tokens
5. **Maintain consistency**: Update when tokens change

## Related Skills

- **visual-design**: Generate AI-powered visual assets for style guides
- **storybook-config**: Configure Storybook for docs-first approach
- **component-scaffold**: Generate components with documentation

## References

- Storybook Docs: https://storybook.js.org/docs/writing-docs
- MDX Format: https://mdxjs.com/
- Doc Blocks: https://storybook.js.org/docs/api/doc-blocks
- Design Systems: https://designsystemchecklist.com/

## Summary

Create comprehensive design system documentation by:
1. Organizing design tokens (colors, typography, spacing)
2. Writing MDX pages with interactive examples
3. Documenting components with usage guidelines
4. Including accessibility notes and best practices
5. Maintaining docs as system evolves

**Result:** A centralized, versioned source of truth for your design system that scales with your team.
