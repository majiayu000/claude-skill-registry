---
name: radflow-component-create
description: Create components that work with RadFlow visual editor and component discovery. Use when building new UI components for projects using RadFlow.
compatibility: Requires RadFlow devtools and components structure
---

# Create RadFlow-Compatible Components

Build components that integrate with RadFlow's visual editor, component discovery, and design system.

## When to Use This Skill

Use this skill when:
- Creating a new UI component for a RadFlow project
- Converting an existing component to be RadFlow-compatible
- Adding variants to an existing component
- Setting up component previews in the Components tab

## Pre-Flight Check

Before creating a new component:

1. **Open RadFlow DevTools** (`Shift+Cmd+K`) -> Components tab
2. **Check if component exists** - Can you extend an existing one?
3. **Check if composable** - Can existing components be combined?

Only create new components when necessary.

## Component Requirements

RadFlow component discovery has strict requirements. All are mandatory.

### 1. Default Export (Required)

```tsx
// Correct - default export
export default function Button({ children }: ButtonProps) {
  return <button>{children}</button>;
}

// Wrong - named export (will not be discovered)
export function Button({ children }: ButtonProps) {
  return <button>{children}</button>;
}
```

### 2. Default Prop Values (Required)

The visual editor renders components without props. All optional props must have defaults.

```tsx
// Correct - all optional props have defaults in destructuring
interface ButtonProps {
  variant?: 'default' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  children: React.ReactNode;  // Required props don't need defaults
}

export default function Button({
  variant = 'default',
  size = 'md',
  disabled = false,
  children
}: ButtonProps) {
  // ...
}

// Wrong - optional props without defaults (visual editor will break)
export default function Button({
  variant,  // undefined causes rendering issues
  size,
  children
}: ButtonProps) {
  // ...
}
```

**Note:** The component scanner extracts default values from destructuring patterns. Defaults defined elsewhere (e.g., `defaultProps`) won't be detected.

### 3. TypeScript Props Interface (Required)

Props must be typed for discovery to extract prop information.

```tsx
// Correct - explicit interface
interface CardProps {
  title?: string;
  children: React.ReactNode;
}

export default function Card({ title = '', children }: CardProps) {
  // ...
}
```

### 4. Location (Required)

**For RadFlow monorepo development:**

| Location | Purpose |
|----------|---------|
| `packages/theme-{name}/components/core/` | Core design system primitives (Button, Card, Input) per theme |
| `packages/theme-{name}/preview/` | Component preview files for DevTools |
| `packages/devtools/src/components/` | DevTools-specific components |

**For consumer projects:**

| Location | Purpose | Tab in DevTools |
|----------|---------|-----------------|
| `/components/ui/` | Design system primitives | "UI" tab |
| `/components/[FolderName]/` | Grouped components | Dynamic folder tab |

**Scanner ignores:** Files matching `.test.`, `.stories.`, or missing default exports.

### 5. Semantic Design Tokens Only (Required)

Use semantic tokens from the `@theme` block. Check RadFlow DevTools -> Variables tab for available tokens.

```tsx
// Correct - semantic tokens (theme-agnostic)
<button className="bg-surface-tertiary text-content-primary border-edge-primary">
<div className="bg-surface-primary border border-edge-primary rounded-md">

// Wrong - brand colors directly (breaks theme switching)
<button className="bg-sun-yellow text-black">

// Wrong - hardcoded Tailwind palette colors
<button className="bg-yellow-400 text-gray-900">
<button className="bg-[#FCE184]">
```

**Semantic token categories:**

| Category | Tokens |
|----------|--------|
| Surfaces | `surface-primary`, `surface-secondary`, `surface-tertiary` |
| Content | `content-primary`, `content-secondary`, `content-inverse` |
| Edges | `edge-primary`, `edge-secondary` |
| Status | `success`, `error`, `warning` |
| Radius | `rounded-none`, `rounded-xs`, `rounded-sm`, `rounded-md`, `rounded-lg`, `rounded-xl`, `rounded-full` |

## Component Template

```tsx
// packages/ui/src/ComponentName.tsx (monorepo)
// or /components/ui/ComponentName.tsx (consumer project)

interface ComponentNameProps {
  variant?: 'default' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  className?: string;
  children: React.ReactNode;
}

export default function ComponentName({
  variant = 'default',
  size = 'md',
  className = '',
  children
}: ComponentNameProps) {
  const variants = {
    default: 'bg-surface-primary border border-edge-primary text-content-primary',
    outline: 'bg-transparent border-2 border-edge-primary text-content-primary',
  };

  const sizes = {
    sm: 'px-2 py-1 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  };

  return (
    <div className={`rounded-md ${variants[variant]} ${sizes[size]} ${className}`}>
      {children}
    </div>
  );
}
```

## Adding Component Previews

Previews enable visual editing in the Components tab. They load **dynamically by folder name**.

### How Preview Loading Works

```
/components/Dashboard/     -> loads ./previews/Dashboard.tsx
/components/Forms/         -> loads ./previews/Forms.tsx
/components/ui/            -> loads ./previews/ui.tsx
```

The file name must **exactly match the folder name** (case-sensitive).

### Step 1: Create Preview File

Create `/devtools/tabs/ComponentsTab/previews/{FolderName}.tsx`:

```tsx
// /devtools/tabs/ComponentsTab/previews/MyComponents.tsx
// File name matches folder: /components/MyComponents/

'use client';

import React from 'react';
import ComponentName from '@/components/MyComponents/ComponentName';
import AnotherComponent from '@/components/MyComponents/AnotherComponent';

// Helper for displaying props
function PropsDisplay({ props }: { props: string }) {
  return (
    <code className="bg-black/5 px-2 py-1 rounded-sm block mt-2 text-sm">
      {props}
    </code>
  );
}

export default function Preview() {
  return (
    <div className="space-y-6">
      {/* Section for ComponentName */}
      <div className="p-4 border border-edge-primary bg-surface-primary rounded">
        <h3 className="mb-3 border-b border-edge-primary/20 pb-2">ComponentName</h3>

        {/* Base component - edits affect all variants */}
        <ComponentName
          variant="default"
          data-edit-scope="component-definition"
          data-component="ComponentName"
        >
          Default variant
        </ComponentName>
        <PropsDisplay props="variant='default'" />

        {/* Variant - edits affect only this variant */}
        <ComponentName
          variant="outline"
          data-edit-scope="component-definition"
          data-component="ComponentName"
          data-edit-variant="outline"
        >
          Outline variant
        </ComponentName>
        <PropsDisplay props="variant='outline'" />

        {/* Size variations - preview only (no data attributes) */}
        <div className="flex gap-2 items-center mt-4">
          <ComponentName size="sm">Small</ComponentName>
          <ComponentName size="md">Medium</ComponentName>
          <ComponentName size="lg">Large</ComponentName>
        </div>
        <PropsDisplay props="size='sm' | 'md' | 'lg'" />
      </div>
    </div>
  );
}
```

### Step 2: Add Tab (if new folder)

If this is a new component folder, add it to tabs via RadFlow UI:
1. Open RadFlow DevTools -> Components tab
2. Click "+" button to add new folder tab
3. Select your folder from dropdown

Or add directly to `/devtools/tabs/ComponentsTab/tabConfig.ts`:

```typescript
export const COMPONENT_TABS: ComponentTabConfig[] = [
  // ... existing tabs
  {
    id: 'folder-MyComponents',  // Must be 'folder-{FolderName}'
    label: 'My Components',
    description: 'Description for this component group',
  },
];
```

## Edit Scope Attributes

These attributes control what gets edited when using the visual editor:

| Attribute Combo | Effect |
|-----------------|--------|
| `data-edit-scope="component-definition"` + `data-component="Name"` | Edits base styles (affects all variants) |
| Above + `data-edit-variant="variantName"` | Edits only that variant's styles |
| No attributes | Preview only, no editing power |

**Key points:**
- Attributes go directly on the component instance, not wrapper divs
- `data-component` value must match the component's file name (without extension)
- Base component (no `data-edit-variant`) edits propagate to all variants unless overridden

## Troubleshooting

### Component not appearing in Components tab?

1. **Check default export** - Must use `export default function`
2. **Check location** - Must be in `/components/` or `/components/{FolderName}/`
3. **Check file name** - Avoid `.test.tsx`, `.stories.tsx` suffixes
4. **Click Refresh** - Scanner runs on demand, not automatically
5. **Check console** - API errors appear in browser DevTools

### Visual editor not rendering component?

1. **Check default props** - All optional props need defaults in destructuring
2. **Check required props** - Provide mock values in preview file
3. **Check imports** - Use `@/components/` alias consistently

### Edits not persisting?

1. **Check data attributes** - Need all three for variant edits
2. **Check component path** - `data-component` must match file name
3. **Check NODE_ENV** - Must be `development`

## Validation Checklist

After creating a component:

- [ ] Default export
- [ ] TypeScript props interface
- [ ] Default values for all optional props (in destructuring)
- [ ] Located in correct directory structure
- [ ] Uses semantic design tokens only (no hardcoded colors)
- [ ] Preview file created (named after folder, not component)
- [ ] Tab added if new folder
- [ ] Component appears in RadFlow DevTools -> Components tab
- [ ] Visual editor can render component without errors

## Common Patterns

### Forwarded Ref (for form components)

```tsx
import { forwardRef } from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

const Input = forwardRef<HTMLInputElement, InputProps>(({
  label = '',
  error = '',
  className = '',
  ...props
}, ref) => {
  return (
    <div>
      {label && <label className="block text-sm font-medium mb-1">{label}</label>}
      <input
        ref={ref}
        className={`w-full px-3 py-2 border rounded-md bg-surface-primary ${error ? 'border-error' : 'border-edge-primary'} ${className}`}
        {...props}
      />
      {error && <p className="text-sm text-error mt-1">{error}</p>}
    </div>
  );
});

Input.displayName = 'Input';
export default Input;
```

### Compound Component

```tsx
import { useState, createContext, useContext } from 'react';

interface AccordionContextValue {
  isOpen: boolean;
  toggle: () => void;
}

const AccordionContext = createContext<AccordionContextValue | null>(null);

interface AccordionProps {
  children: React.ReactNode;
  defaultOpen?: boolean;
}

function Accordion({ children, defaultOpen = false }: AccordionProps) {
  const [isOpen, setIsOpen] = useState(defaultOpen);
  return (
    <AccordionContext.Provider value={{ isOpen, toggle: () => setIsOpen(!isOpen) }}>
      <div className="border border-edge-primary rounded-md bg-surface-primary">{children}</div>
    </AccordionContext.Provider>
  );
}

Accordion.Trigger = function AccordionTrigger({ children }: { children: React.ReactNode }) {
  const ctx = useContext(AccordionContext);
  return (
    <button onClick={ctx?.toggle} className="w-full p-3 text-left font-medium text-content-primary">
      {children}
    </button>
  );
};

Accordion.Content = function AccordionContent({ children }: { children: React.ReactNode }) {
  const ctx = useContext(AccordionContext);
  if (!ctx?.isOpen) return null;
  return <div className="p-3 border-t border-edge-primary">{children}</div>;
};

export default Accordion;
```

### Polymorphic Component

```tsx
type PolymorphicProps<T extends React.ElementType> = {
  as?: T;
  variant?: 'filled' | 'outline';
  children: React.ReactNode;
} & Omit<React.ComponentPropsWithoutRef<T>, 'as' | 'variant' | 'children'>;

export default function Button<T extends React.ElementType = 'button'>({
  as,
  variant = 'filled',
  children,
  ...props
}: PolymorphicProps<T>) {
  const Component = as || 'button';
  const variants = {
    filled: 'bg-surface-tertiary text-content-primary border border-edge-primary',
    outline: 'bg-transparent border-2 border-edge-primary text-content-primary',
  };
  return (
    <Component className={`px-4 py-2 rounded-md ${variants[variant]}`} {...props}>
      {children}
    </Component>
  );
}
```
