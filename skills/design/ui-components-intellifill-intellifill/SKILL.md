---
name: ui-components
description: UI component generation patterns for IntelliFill. Replaces magic/21st.dev MCP to save ~3.4k tokens.
---

# UI Components

This skill covers component creation patterns for IntelliFill's React frontend. It replaces the 21st.dev/magic MCP server with lazy-loaded guidance.

## When I Need This

- Creating new React components
- Building forms with validation
- Adding modal dialogs
- Creating data tables
- Implementing loading states

## Component Stack

IntelliFill uses: React 18, Radix UI, TailwindCSS 4.0, CVA for variants, Zustand for state.

## File Location

New components go in `quikadmin-web/src/components/` with structure:
```
components/
├── ui/           # Base primitives (Button, Input, Dialog)
├── forms/        # Form-related (ProfileForm, UploadForm)
├── documents/    # Document-specific (DocumentList, DocumentViewer)
└── layout/       # Layout (Sidebar, Header, ProtectedRoute)
```

## Component Template

```tsx
// quikadmin-web/src/components/ui/ComponentName.tsx
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const componentVariants = cva(
  'base-classes-here',
  {
    variants: {
      variant: {
        default: 'variant-default-classes',
        secondary: 'variant-secondary-classes',
      },
      size: {
        sm: 'text-sm px-2 py-1',
        md: 'text-base px-4 py-2',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'md',
    },
  }
);

interface Props extends VariantProps<typeof componentVariants> {
  children: React.ReactNode;
  className?: string;
}

export function ComponentName({ variant, size, className, children }: Props) {
  return (
    <div className={cn(componentVariants({ variant, size }), className)}>
      {children}
    </div>
  );
}
```

## Common Patterns

### Form Field
```tsx
<div className="space-y-2">
  <Label htmlFor="field">Label</Label>
  <Input id="field" placeholder="Placeholder" {...register('field')} />
  {errors.field && <p className="text-sm text-red-500">{errors.field.message}</p>}
</div>
```

### Modal Dialog
```tsx
<Dialog open={open} onOpenChange={setOpen}>
  <DialogTrigger asChild>
    <Button>Open</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Title</DialogTitle>
      <DialogDescription>Description</DialogDescription>
    </DialogHeader>
    {/* Content */}
    <DialogFooter>
      <Button onClick={() => setOpen(false)}>Close</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

### Loading State
```tsx
{isLoading ? (
  <div className="flex items-center justify-center p-8">
    <Loader2 className="h-8 w-8 animate-spin text-primary" />
  </div>
) : (
  <>{/* Content */}</>
)}
```

## Existing UI Components

Check `quikadmin-web/src/components/ui/` for existing primitives before creating new ones. We have: Button, Input, Label, Dialog, Select, Card, Table, Tabs, Toast.

## For Inspiration

If you need design inspiration for a component, use Web Search to find examples or check the existing components in the codebase first.
