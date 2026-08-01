---
name: component-integration
description: React, MDX, and Tailwind CSS integration patterns for Astro websites.
  Use when adding React components, configuring MDX content, setting up Tailwind styling,
  integrating component libraries, building
---

---
name: component-integration
description: React, MDX, and Tailwind CSS integration patterns for Astro websites. Use when adding React components, configuring MDX content, setting up Tailwind styling, integrating component libraries, building interactive UI elements, or when user mentions React integration, MDX setup, Tailwind configuration, component patterns, or UI frameworks.
allowed-tools: - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Component Integration

Comprehensive patterns for integrating React components, MDX content, and Tailwind CSS into Astro websites with type safety, performance optimization, and best practices.

## Overview

This skill provides:
- React component integration with Astro islands architecture
- MDX configuration for content-rich component authoring
- Tailwind CSS setup with custom design systems
- Type-safe component patterns with TypeScript
- Performance optimization techniques
- Component library integration (shadcn/ui, Radix, etc.)

## Setup Scripts

### Core Setup Scripts

1. **scripts/setup-react.sh** - Initialize React integration in Astro project
2. **scripts/setup-mdx.sh** - Configure MDX support with plugins
3. **scripts/setup-tailwind.sh** - Install and configure Tailwind CSS
4. **scripts/validate-integration.sh** - Validate component integration setup
5. **scripts/optimize-components.sh** - Apply performance optimizations

### Utility Scripts

6. **scripts/generate-component.sh** - Scaffold new React components
7. **scripts/add-component-library.sh** - Integrate shadcn/ui or other libraries

## Templates

### React Component Templates

1. **templates/react/basic-component.tsx** - Simple React component with TypeScript
2. **templates/react/interactive-component.tsx** - Interactive component with state
3. **templates/react/island-component.tsx** - Astro island with client directives
4. **templates/react/form-component.tsx** - Form component with validation
5. **templates/react/data-fetching-component.tsx** - Component with async data
6. **templates/react/component-with-context.tsx** - Context provider pattern

### MDX Templates

7. **templates/mdx/basic-mdx.mdx** - Basic MDX file structure
8. **templates/mdx/mdx-with-components.mdx** - MDX using custom components
9. **templates/mdx/mdx-layout.astro** - Layout wrapper for MDX content
10. **templates/mdx/remark-plugin.js** - Custom remark plugin template

### Tailwind Templates

11. **templates/tailwind/tailwind.config.ts** - Full Tailwind configuration
12. **templates/tailwind/custom-theme.ts** - Custom design system theme
13. **templates/tailwind/base-styles.css** - Base CSS with custom utilities
14. **templates/tailwind/component-variants.ts** - CVA variant patterns

### Integration Templates

15. **templates/integration/astro-config-full.ts** - Complete Astro config
16. **templates/integration/tsconfig-components.json** - TypeScript config for components
17. **templates/integration/package-json-deps.json** - Required dependencies

## Examples

1. **examples/basic-integration.md** - Simple React component in Astro
2. **examples/mdx-blog-post.md** - MDX blog post with components
3. **examples/tailwind-design-system.md** - Custom Tailwind design system
4. **examples/interactive-forms.md** - Forms with validation and state
5. **examples/component-library-integration.md** - shadcn/ui setup guide
6. **examples/performance-optimization.md** - Islands architecture best practices
7. **examples/type-safe-patterns.md** - TypeScript patterns for components

## Instructions

### Phase 1: Initial Setup

1. **Assess Current Setup**
   ```bash
   # Check existing integrations
   bash scripts/validate-integration.sh
   ```

2. **Install Required Integrations**
   ```bash
   # Setup React
   bash scripts/setup-react.sh

   # Setup MDX
   bash scripts/setup-mdx.sh

   # Setup Tailwind
   bash scripts/setup-tailwind.sh
   ```

3. **Validate Installation**
   - Check astro.config.mjs for integrations
   - Verify package.json dependencies
   - Test basic component rendering

### Phase 2: Component Development

1. **Generate Component Structure**
   ```bash
   # Create new component
   bash scripts/generate-component.sh ComponentName --type interactive
   ```

2. **Apply Templates**
   - Use templates/react/* for React components
   - Use templates/mdx/* for content components
   - Use templates/tailwind/* for styling patterns

3. **Implement Type Safety**
   - Define component props interfaces
   - Use TypeScript strict mode
   - Export component types for consumers

### Phase 3: Styling Integration

1. **Configure Tailwind Theme**
   - Read: templates/tailwind/tailwind.config.ts
   - Customize colors, fonts, spacing
   - Add custom utilities and variants

2. **Create Component Variants**
   - Use CVA (class-variance-authority) pattern
   - Read: templates/tailwind/component-variants.ts
   - Define size, color, and style variants

3. **Setup Base Styles**
   - Read: templates/tailwind/base-styles.css
   - Add custom CSS variables
   - Define global typography styles

### Phase 4: MDX Configuration

1. **Setup MDX Processing**
   - Configure remark and rehype plugins
   - Read: templates/mdx/remark-plugin.js
   - Add syntax highlighting, image optimization

2. **Create MDX Layouts**
   - Read: templates/mdx/mdx-layout.astro
   - Design consistent content layouts
   - Add frontmatter-based customization

3. **Register Custom Components**
   - Map components to MDX elements
   - Read: templates/mdx/mdx-with-components.mdx
   - Enable rich content authoring

### Phase 5: Performance Optimization

1. **Apply Islands Architecture**
   - Use client:* directives strategically
   - Read: examples/performance-optimization.md
   - Minimize client JavaScript

2. **Optimize Component Loading**
   ```bash
   bash scripts/optimize-components.sh
   ```

3. **Implement Code Splitting**
   - Use dynamic imports for heavy components
   - Lazy load below-the-fold content
   - Defer non-critical interactions

### Phase 6: Component Library Integration

1. **Add Component Libraries**
   ```bash
   # Add shadcn/ui
   bash scripts/add-component-library.sh shadcn-ui
   ```

2. **Configure Library Theming**
   - Integrate library tokens with Tailwind
   - Customize component defaults
   - Ensure consistent design language

3. **Create Wrapper Components**
   - Wrap library components for Astro compatibility
   - Add project-specific defaults
   - Maintain type safety

## Best Practices

### React Integration

- **Use Islands Architecture**: Only hydrate interactive components
- **Minimize Bundle Size**: Import only needed components
- **Type Everything**: Use TypeScript interfaces for all props
- **Avoid Layout Shift**: Reserve space for hydrated components
- **Handle SSR**: Ensure components work server-side

### MDX Content

- **Separate Content from Logic**: Keep MDX focused on content
- **Use Frontmatter**: Add metadata for routing and SEO
- **Component Consistency**: Reuse components across MDX files
- **Optimize Images**: Use Astro Image optimization
- **Test Rendering**: Validate MDX compiles correctly

### Tailwind Styling

- **Design Tokens**: Define colors, spacing in config
- **Utility Classes**: Prefer utilities over custom CSS
- **Component Variants**: Use CVA for variant management
- **Responsive Design**: Mobile-first approach
- **Dark Mode**: Configure dark mode variant strategy

### Performance

- **Static First**: Generate static HTML by default
- **Selective Hydration**: Use client:visible, client:idle
- **Bundle Analysis**: Monitor JavaScript bundle sizes
- **CSS Optimization**: Purge unused Tailwind classes
- **Image Optimization**: Use Astro Image component

## Common Patterns

### Pattern 1: Interactive Island Component

```tsx
// Component with selective hydration
import { useState } from 'react';

interface Props {
  initialCount?: number;
}

export default function Counter({ initialCount = 0 }: Props) {
  const [count, setCount] = useState(initialCount);

  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  );
}
```

Usage in Astro:
```astro
---
import Counter from '@/components/Counter';
---
<Counter client:visible initialCount={5} />
```

### Pattern 2: MDX with Custom Components

```mdx
---
title: "Blog Post with Components"
---
import { Alert } from '@/components/Alert';

# My Blog Post

<Alert type="info">
  This is custom component in MDX
</Alert>
```

### Pattern 3: Tailwind Variant Component

```tsx
import { cva, type VariantProps } from 'class-variance-authority';

const buttonVariants = cva(
  'rounded-md font-medium transition-colors'
  {
    variants: {
      variant: {
        primary: 'bg-blue-600 text-white hover:bg-blue-700'
        secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300'
      }
      size: {
        sm: 'px-3 py-1.5 text-sm'
        md: 'px-4 py-2 text-base'
        lg: 'px-6 py-3 text-lg'
      }
    }
    defaultVariants: {
      variant: 'primary'
      size: 'md'
    }
  }
);

type ButtonProps = VariantProps<typeof buttonVariants> & {
  children: React.ReactNode;
};

export function Button({ variant, size, children }: ButtonProps) {
  return (
    <button className={buttonVariants({ variant, size })}>
      {children}
    </button>
  );
}
```

## Troubleshooting

### React Components Not Hydrating

**Problem**: Components render statically but don't have interactivity

**Solution**:
1. Add client directive: `client:load`, `client:visible`, or `client:idle`
2. Ensure component is exported as default
3. Check for SSR-incompatible code (window, document)

### MDX Compilation Errors

**Problem**: MDX files fail to compile

**Solution**:
1. Validate MDX syntax (closing tags, component imports)
2. Check remark/rehype plugin compatibility
3. Ensure imported components are available
4. Review astro.config.mjs MDX configuration

### Tailwind Classes Not Applied

**Problem**: Tailwind utilities not working in components

**Solution**:
1. Check tailwind.config.ts content paths include component files
2. Import Tailwind base styles in layout
3. Verify PostCSS configuration
4. Clear Astro cache: `rm -rf .astro`

### Type Errors in Components

**Problem**: TypeScript errors in React components

**Solution**:
1. Review templates/integration/tsconfig-components.json
2. Ensure @types/react is installed
3. Check jsx compiler options
4. Validate component prop interfaces

## Related Skills

- **content-collections**: Use for structured content with type safety
- **performance-optimization**: Additional performance patterns
- **testing-patterns**: Testing React components in Astro

## Requirements

- Node.js 18+
- Astro 4.0+
- React 18+
- Tailwind CSS 3.4+
- TypeScript 5.0+

---

**Plugin**: website-builder
**Version**: 1.0.0
