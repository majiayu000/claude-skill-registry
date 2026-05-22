---
name: frontend-ui-components
description: Provides guidelines for using shared UI components and styling. This skill should be used when implementing UI features using Shadcn/Radix components and the shared @eridu/ui package.
---

# Frontend UI Components

This skill outlines how to build and use UI components in the frontend applications, leveraging the shared `@eridu/ui` package and Shadcn patterns.

## The `@eridu/ui` Package

All generic UI components (Buttons, Inputs, Dialogs, etc.) live in `packages/ui`. Do NOT create local copies of generic components in apps.

### Usage

```typescript
import { Button } from '@eridu/ui/components/button';
import { Input } from '@eridu/ui/components/input';

export function MyForm() {
  return (
    <div className="flex gap-4">
      <Input placeholder="Search..." />
      <Button variant="default">Search</Button>
    </div>
  );
}
```

## Styling Pattern (Tailwind CSS v4)

We use **Tailwind CSS v4** with `clsx` and `tailwind-merge` for conditional styling.

### The `cn` Utility

Use the `cn` utility from `@eridu/ui/lib/utils` to merge classes safely.

```typescript
import { cn } from '@eridu/ui/lib/utils';

interface CardProps {
  className?: string;
  children: React.ReactNode;
}

export function Card({ className, children }: CardProps) {
  return (
    <div className={cn("rounded-lg border bg-card text-card-foreground shadow-sm", className)}>
      {children}
    </div>
  );
}
```

## Component Design Patterns

### Composition Over Large Components

Build complex UIs by composing small, focused components instead of creating large monolithic components.

**Benefits**:
- Easier to test and maintain
- Better performance (smaller re-render scope)
- More reusable components
- Clearer separation of concerns

```typescript
// ❌ BAD: Large monolithic component
function UserDashboard() {
  return (
    <div>
      <header>{/* Complex header logic */}</header>
      <nav>{/* Complex navigation */}</nav>
      <main>
        <div>{/* User stats */}</div>
        <div>{/* Activity feed */}</div>
        <div>{/* Recommendations */}</div>
      </main>
      <footer>{/* Footer content */}</footer>
    </div>
  );
}

// ✅ GOOD: Composed from smaller components
function UserDashboard() {
  return (
    <div>
      <DashboardHeader />
      <DashboardNav />
      <main>
        <UserStats />
        <ActivityFeed />
        <Recommendations />
      </main>
      <DashboardFooter />
    </div>
  );
}
```

### Using Children for Composition

Use the `children` prop to create flexible, composable components.

```typescript
// Flexible Dialog component using composition
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@eridu/ui/components/dialog';

function ConfirmDeleteDialog({ isOpen, onClose, onConfirm }) {
  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Confirm Deletion</DialogTitle>
        </DialogHeader>
        <p>Are you sure you want to delete this item?</p>
        <div className="flex gap-2">
          <Button variant="outline" onClick={onClose}>Cancel</Button>
          <Button variant="destructive" onClick={onConfirm}>Delete</Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}
```

### Wrapping 3rd Party Components

Wrap 3rd party components to adapt them to your application's needs and make future changes easier.

```typescript
// Wrap Radix Link to add app-specific behavior
import { Link as RadixLink } from '@radix-ui/react-navigation-menu';
import { cn } from '@eridu/ui/lib/utils';

interface AppLinkProps extends React.ComponentPropsWithoutRef<typeof RadixLink> {
  external?: boolean;
}

export function Link({ external, className, children, ...props }: AppLinkProps) {
  return (
    <RadixLink
      className={cn('text-primary hover:underline', className)}
      target={external ? '_blank' : undefined}
      rel={external ? 'noopener noreferrer' : undefined}
      {...props}
    >
      {children}
      {external && <span className="ml-1">↗</span>}
    </RadixLink>
  );
}
```

### When to Abstract Components

Abstract components into the shared `@eridu/ui` package when:

1. **Used in multiple apps** - Component is needed across `erify_creators`, `erify_studios`, etc.
2. **Generic and reusable** - Not tied to specific business logic
3. **Stable API** - Interface is unlikely to change frequently
4. **Well-tested** - Component has proper tests and documentation

**Don't abstract too early**:
- Wait until you have 2-3 use cases before abstracting
- Avoid premature abstraction (wrong abstractions are worse than duplication)
- Keep feature-specific components in feature folders

## Creating New Components

When creating **app-specific** features:
1.  Compose them using primitives from `@eridu/ui`.
2.  Keep them in `src/components/{feature-name}/`.

When creating **new generic** primitives:
1.  Add them to `packages/ui/src/components/`.
2.  Follow the Radix UI + Tailwind pattern (Shadcn style).
3.  Export them via `packages/ui/package.json`.

## Checklist

- [ ] Import generic components from `@eridu/ui`.
- [ ] Use `cn()` for class merging.
- [ ] Ensure components are accessible (Radix UI primitives).
- [ ] Use Tailwind text/bg colors that map to the theme (e.g., `bg-primary`, `text-muted-foreground`).
