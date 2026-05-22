---
name: ui-component
slug: ui-component
version: 1.0.0
category: core
description: Generate design-compliant React components using shadcn/ui primitives and design tokens
triggers:
  - pattern: "component|card|form|button|modal|dialog|table|list|nav|menu|accordion|tabs|input|select|checkbox|radio|switch|slider|dropdown|tooltip|popover|alert|badge|avatar|progress|skeleton|separator|sheet|toast|calendar|combobox"
    confidence: 0.8
    examples:
      - "create a card component"
      - "build a modal dialog"
      - "I need a form component"
      - "generate a button"
      - "create a navigation menu"
      - "build a data table"
      - "create a dropdown menu"
      - "generate an accordion"
mcp_dependencies:
  - server: context7
    required: false
    capabilities:
      - "search"
---

# UI Component Skill

Automatically generate production-ready, design-compliant React components using shadcn/ui primitives and Turbocat design tokens. This skill transforms natural language component requirements into fully functional, accessible, and styled React components that seamlessly integrate with the existing design system.

## Overview

This skill generates:
- **Design-compliant React components** (TypeScript)
- **shadcn/ui primitive integration** (Radix UI-based)
- **Design token compliance** (uses lib/design-tokens.ts)
- **Accessibility features** (WCAG AA compliance)
- **TypeScript type definitions** (props interfaces)
- **Component Gallery integration** (reads and contributes)
- **Storybook stories** (optional documentation)

## When to Use This Skill

Activate this skill when the user requests:
- Component creation or generation
- UI elements (buttons, cards, forms, modals, etc.)
- Interactive widgets
- Navigation components
- Form inputs and controls
- Data display components
- Layout components
- Feedback components (alerts, toasts, progress)

## Key Features

### 1. Design System Compliance

All generated components follow the Turbocat design system:

```typescript
// Components use design tokens
import { colors, spacing, borderRadius } from '@/lib/design-tokens'

// Or Tailwind classes that map to design tokens
<button className="bg-orange-500 text-white rounded-md px-4 py-2">
  Primary Action
</button>
```

**Color Usage:**
- `orange-500` - Primary actions, brand elements
- `blue-500` - Links, secondary actions, info states
- `gray-*` - Neutral UI elements, backgrounds, borders
- Semantic colors - Success, warning, error, info states

### 2. shadcn/ui Integration

Leverages existing shadcn/ui components as building blocks:

```typescript
// Uses Radix UI primitives
import * as Dialog from '@radix-ui/react-dialog'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'

// Extends existing components
import { buttonVariants } from '@/components/ui/button'

const CustomButton = ({ variant = 'default', ...props }) => (
  <button className={cn(buttonVariants({ variant }))} {...props} />
)
```

**Available Primitives:**
- Accordion
- Alert Dialog
- Avatar
- Badge
- Button
- Card
- Checkbox
- Dialog
- Dropdown Menu
- Input
- Label
- Progress
- Radio Group
- Select
- Switch
- Tabs
- Textarea
- Tooltip

### 3. Component Gallery Integration

Reads from and contributes to the component gallery:

**Reading Existing Components:**
- Scans `components/ui/` directory
- Identifies similar components to avoid duplication
- References existing patterns for consistency
- Suggests extending existing components vs creating new ones

**Contributing New Components:**
- Generates component metadata
- Adds to appropriate directory structure
- Creates optional Storybook stories
- Documents component API

### 4. Accessibility (WCAG AA)

All components include accessibility features:

**Keyboard Navigation:**
- Tab order management
- Arrow key navigation (where applicable)
- Escape to close (modals, dropdowns)
- Enter/Space for activation

**ARIA Attributes:**
- `role` attributes for semantic meaning
- `aria-label`, `aria-labelledby` for screen readers
- `aria-expanded`, `aria-selected` for states
- `aria-describedby` for descriptions

**Visual Accessibility:**
- Color contrast ratios ≥ 4.5:1 for text
- Focus indicators on all interactive elements
- Dark mode support with proper contrast
- Screen reader-friendly markup

**Example:**
```typescript
<button
  className="focus-visible:ring-2 focus-visible:ring-orange-500"
  aria-label="Submit form"
  type="submit"
>
  Submit
</button>
```

### 5. TypeScript Support

Full TypeScript integration with type safety:

```typescript
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'destructive' | 'outline' | 'secondary' | 'ghost' | 'link'
  size?: 'default' | 'sm' | 'lg' | 'icon'
  asChild?: boolean
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant = 'default', size = 'default', ...props }, ref) => {
    // Implementation
  }
)

Button.displayName = 'Button'
```

## Component Types

### Layout Components
- Card
- Container
- Grid
- Stack
- Separator
- Divider

### Form Components
- Input
- Textarea
- Select
- Checkbox
- Radio Group
- Switch
- Slider
- Combobox

### Navigation Components
- Navigation Menu
- Tabs
- Breadcrumb
- Pagination
- Command Menu

### Feedback Components
- Alert
- Toast
- Progress
- Skeleton
- Badge
- Avatar

### Overlay Components
- Modal/Dialog
- Drawer
- Sheet
- Popover
- Tooltip
- Dropdown Menu
- Alert Dialog

### Data Display
- Table
- List
- Card Grid
- Calendar
- Data Grid

## Execution Steps

When this skill is activated:

1. **Parse Component Requirements**
   - Extract component type from prompt
   - Identify required features and props
   - Determine if similar component exists
   - Check for duplicate components

2. **Read Component Gallery**
   - Scan `components/ui/` for existing components
   - Identify similar patterns to reference
   - Check shadcn/ui primitives availability
   - Determine if extension vs new component

3. **Generate Component Code**
   - Import required dependencies (Radix UI, utils)
   - Apply design tokens via Tailwind classes
   - Add TypeScript interfaces for props
   - Include accessibility attributes
   - Add proper ref forwarding if needed
   - Export component with displayName

4. **Apply Design Tokens**
   - Use `orange-500` for primary actions
   - Use `blue-500` for links/secondary actions
   - Apply proper spacing from design tokens
   - Use border radius from design system
   - Add animation transitions

5. **Ensure Accessibility**
   - Add ARIA attributes
   - Include keyboard event handlers
   - Ensure focus management
   - Verify color contrast
   - Add screen reader support

6. **Generate Metadata**
   - Component name and type
   - File path in components directory
   - Props documentation
   - Usage examples
   - Dependencies list

7. **Optional: Generate Storybook Story**
   - Create story file
   - Add multiple variants
   - Include controls for props
   - Add accessibility addon config

## Usage Examples

### Example 1: Simple Button Component

**User Prompt:**
"Create a loading button component"

**Generated Output:**
```typescript
// components/ui/loading-button.tsx
import * as React from 'react'
import { Button, buttonVariants } from '@/components/ui/button'
import { cn } from '@/lib/utils'

interface LoadingButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  loading?: boolean
  variant?: 'default' | 'destructive' | 'outline' | 'secondary' | 'ghost' | 'link'
  size?: 'default' | 'sm' | 'lg' | 'icon'
}

export const LoadingButton = React.forwardRef<HTMLButtonElement, LoadingButtonProps>(
  ({ loading = false, children, disabled, className, variant, size, ...props }, ref) => {
    return (
      <Button
        ref={ref}
        disabled={disabled || loading}
        variant={variant}
        size={size}
        className={cn(className)}
        {...props}
      >
        {loading && (
          <svg
            className="mr-2 h-4 w-4 animate-spin"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
        )}
        <span className={cn(loading && 'opacity-70')}>{children}</span>
      </Button>
    )
  }
)

LoadingButton.displayName = 'LoadingButton'
```

### Example 2: Complex Form Component

**User Prompt:**
"Create a user profile form with validation"

**Generated Output:**
- Form component with controlled inputs
- Zod schema for validation
- Error message display
- Accessibility labels
- Design token colors

### Example 3: Data Display Component

**User Prompt:**
"Create a stat card component for dashboard"

**Generated Output:**
```typescript
// components/ui/stat-card.tsx
import * as React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { cn } from '@/lib/utils'

interface StatCardProps {
  title: string
  value: string | number
  description?: string
  trend?: 'up' | 'down' | 'neutral'
  trendValue?: string
  icon?: React.ReactNode
  className?: string
}

export function StatCard({
  title,
  value,
  description,
  trend,
  trendValue,
  icon,
  className,
}: StatCardProps) {
  return (
    <Card className={cn('overflow-hidden', className)}>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        {icon && <div className="text-muted-foreground">{icon}</div>}
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        {description && (
          <p className="text-xs text-muted-foreground mt-1">{description}</p>
        )}
        {trend && trendValue && (
          <div className="flex items-center mt-2">
            <span
              className={cn(
                'text-xs font-medium',
                trend === 'up' && 'text-green-600',
                trend === 'down' && 'text-red-600',
                trend === 'neutral' && 'text-gray-600'
              )}
            >
              {trend === 'up' && '↑'}
              {trend === 'down' && '↓'}
              {trend === 'neutral' && '→'}
              {' '}
              {trendValue}
            </span>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
```

## Design Token Mapping

The skill automatically maps component variants to design tokens:

| Component Part | Design Token | Tailwind Class |
|---------------|--------------|----------------|
| Primary Button | orange-500 | `bg-orange-500` |
| Link/Secondary | blue-500 | `text-blue-500` |
| Success State | semantic.success | `text-green-600` |
| Error State | semantic.error | `text-red-600` |
| Border Radius | borderRadius.md | `rounded-md` |
| Spacing | spacing[4] | `p-4`, `m-4` |
| Focus Ring | orange-500 | `focus-visible:ring-orange-500` |

## MCP Integration

### Context7 (Optional)

When Context7 MCP is available:
- Search for existing components in codebase
- Find similar component patterns
- Reference component documentation
- Discover component usage examples

## Best Practices

### Component Structure

```typescript
// 1. Imports
import * as React from 'react'
import { cn } from '@/lib/utils'

// 2. Type definitions
interface ComponentProps {
  // Props here
}

// 3. Component implementation
export const Component = React.forwardRef<HTMLElement, ComponentProps>(
  ({ className, ...props }, ref) => {
    // Implementation
  }
)

// 4. Display name
Component.displayName = 'Component'
```

### Styling Guidelines

- Use Tailwind classes that map to design tokens
- Prefer design system colors over arbitrary values
- Use `cn()` utility for className merging
- Include dark mode variants with `dark:` prefix
- Add hover and focus states for interactive elements

### Accessibility Checklist

- [ ] Semantic HTML elements
- [ ] ARIA attributes where needed
- [ ] Keyboard navigation support
- [ ] Focus management
- [ ] Color contrast ≥ 4.5:1
- [ ] Screen reader friendly
- [ ] Touch target size ≥ 44x44px

## Limitations

- Components must use React 18+ features
- Requires shadcn/ui setup in project
- Tailwind CSS required for styling
- TypeScript required for type safety

## Future Enhancements

- AI-powered component variant suggestions
- Automatic responsive design generation
- Component composition recommendations
- Performance optimization suggestions
- Advanced animation integration
- Component testing generation
- Visual regression testing

---

**Skill Version:** 1.0.0
**Last Updated:** 2026-01-04
**Maintainer:** Turbocat Agent System
