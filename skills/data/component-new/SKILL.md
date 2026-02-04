---
name: component-new
description: "Create a new React component with TypeScript and modern best practices"
---

# Create New Component

Generate a new React component following 2025 best practices.

## Component Specification

$ARGUMENTS

## Modern React + TypeScript Standards

### 1. **Function Components Only**
- Use function components (not class components)
- React 19 patterns
- Server Components where appropriate (Next.js)

### 2. **TypeScript Best Practices**
- Strict typing (`strict: true`)
- Interface for props
- Proper TypeScript utility types (ComponentProps, ReactNode, etc.)
- NO `any` types
- Explicit return types for complex components

### 3. **Component Patterns**

**Client Components** (interactive, use hooks)
```typescript
'use client'
import { useState } from 'react'

interface Props {
  // typed props
}

export function Component({ }: Props) {
  // implementation
}
```

**Server Components** (default in Next.js App Router)
```typescript
interface Props {
  // typed props
}

export async function Component({ }: Props) {
  // can fetch data directly
}
```

### 4. **State Management**
- `useState` for local state
- `useReducer` for complex state
- Zustand for global state
- React Context for theme/auth

### 5. **Performance**
- Lazy loading with `React.lazy()`
- Code splitting
- `useMemo()` for expensive computations
- `useCallback()` for callback functions

### 6. **Styling Approach** (choose based on project)
- **Tailwind CSS** - Utility-first (recommended)
- **CSS Modules** - Scoped styles
- **Styled Components** - CSS-in-JS

## What to Generate

1. **Component File** - Main component with TypeScript
2. **Props Interface** - Fully typed props
3. **Styles** - Tailwind classes or CSS module
4. **Example Usage** - How to import and use
5. **Storybook Story** (optional) - Component documentation

## Code Quality Standards

**Structure**
- Feature-based folder organization
- Co-locate related files
- Barrel exports (index.ts)
- Clear file naming conventions

**TypeScript**
- Explicit prop types via interface
- Proper generics where needed
- Utility types (Pick, Omit, Partial)
- Discriminated unions for variants

**Props**
- Required vs optional props
- Default values where appropriate
- Destructure in function signature
- Props spread carefully

**Accessibility**
- Semantic HTML
- ARIA labels where needed
- Keyboard navigation
- Screen reader friendly

**Best Practices**
- Single Responsibility Principle
- Composition over inheritance
- Extract complex logic to hooks
- Keep components small (<200 lines)

## Component Types to Consider

**Presentational Components**
- Pure UI rendering
- No business logic
- Receive data via props
- Easy to test

**Container Components**
- Data fetching
- Business logic
- State management
- Pass data to presentational components

**Compound Components**
- Related components working together
- Shared context
- Flexible API
- Example: `<Select><Select.Trigger/><Select.Content/></Select>`

## React 19 Features to Use

- **use()** API for reading promises/context
- **useActionState()** for form state
- **useFormStatus()** for form pending state
- **useOptimistic()** for optimistic UI updates
- **Server Actions** for mutations

Generate production-ready, accessible, and performant React components following Next.js 15 and React 19 patterns.
