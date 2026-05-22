---
name: frontend-design-fixlify
description: Create distinctive, production-grade frontend interfaces for Fixlify. Automatically activates when building UI components, pages, dashboards, forms, or any visual interface. Uses Fixlify design system with shadcn/ui, Tailwind CSS, and React patterns.
version: 1.0.0
author: Fixlify Team
tags: [frontend, ui, design, react, tailwind, shadcn]
---

# Fixlify Frontend Design Skill

Create distinctive, production-grade interfaces for Fixlify field service management platform. Every UI should feel professional, modern, and purpose-built for service professionals and field teams.

## Fixlify Design System

### Brand Identity
```
Primary Violet:  #8b5cf6 (violet-500)
Primary Dark:    #7c3aed (violet-600)
Success Green:   #22c55e (green-500) / #10b981 (emerald-500)
Warning Amber:   #f59e0b (amber-500)
Error Red:       #ef4444 (red-500)
Background:      #ffffff / #0f172a (dark)
Surface:         #f8fafc / #1e293b (dark)
Border:          #e2e8f0 / #334155 (dark)

Primary Button:  bg-violet-600 hover:bg-violet-700 text-white
Outline Button:  text-violet-600 border-violet-200 hover:bg-violet-50
Hover Effects:   hover:border-violet-200 hover:shadow-violet-50
```

### Typography
```css
/* Headings - Inter or System */
font-family: 'Inter', system-ui, sans-serif;

/* Hierarchy */
h1: text-3xl font-bold tracking-tight
h2: text-2xl font-semibold
h3: text-xl font-semibold
h4: text-lg font-medium
body: text-sm text-muted-foreground
```

### Spacing System
```
Base unit: 4px (Tailwind default)
Component padding: p-4 to p-6
Card gaps: gap-4 to gap-6
Section spacing: space-y-6 to space-y-8
```

## Tech Stack

```typescript
// Core
import React from 'react';
import { cn } from '@/lib/utils';

// UI Components (shadcn/ui)
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem } from '@/components/ui/dropdown-menu';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { toast } from 'sonner';

// Icons (Lucide)
import { Plus, Search, Filter, MoreHorizontal, Edit, Trash2, Check, X } from 'lucide-react';

// Forms
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';

// Data Fetching
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
```

## Component Patterns

### Page Layout
```tsx
export function ExamplePage() {
  return (
    <div className="flex flex-col gap-6 p-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Page Title</h1>
          <p className="text-muted-foreground">Description of this page</p>
        </div>
        <Button>
          <Plus className="mr-2 h-4 w-4" />
          Add New
        </Button>
      </div>

      {/* Filters */}
      <div className="flex items-center gap-4">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input placeholder="Search..." className="pl-10" />
        </div>
        <Button variant="outline" size="icon">
          <Filter className="h-4 w-4" />
        </Button>
      </div>

      {/* Content */}
      <Card>
        <CardContent className="p-0">
          {/* Table or content here */}
        </CardContent>
      </Card>
    </div>
  );
}
```

### Data Table
```tsx
<Table>
  <TableHeader>
    <TableRow>
      <TableHead>Name</TableHead>
      <TableHead>Status</TableHead>
      <TableHead>Date</TableHead>
      <TableHead className="w-[50px]"></TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    {items.map((item) => (
      <TableRow key={item.id} className="cursor-pointer hover:bg-muted/50">
        <TableCell className="font-medium">{item.name}</TableCell>
        <TableCell>
          <Badge variant={getStatusVariant(item.status)}>
            {item.status}
          </Badge>
        </TableCell>
        <TableCell>{formatDate(item.created_at)}</TableCell>
        <TableCell>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="icon">
                <MoreHorizontal className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem>
                <Edit className="mr-2 h-4 w-4" />
                Edit
              </DropdownMenuItem>
              <DropdownMenuItem className="text-destructive">
                <Trash2 className="mr-2 h-4 w-4" />
                Delete
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </TableCell>
      </TableRow>
    ))}
  </TableBody>
</Table>
```

### Form Pattern
```tsx
const formSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  email: z.string().email('Invalid email'),
  phone: z.string().optional(),
});

type FormData = z.infer<typeof formSchema>;

export function ExampleForm({ onSubmit }: { onSubmit: (data: FormData) => void }) {
  const form = useForm<FormData>({
    resolver: zodResolver(formSchema),
    defaultValues: { name: '', email: '', phone: '' },
  });

  return (
    <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="name">Name</Label>
        <Input
          id="name"
          {...form.register('name')}
          className={cn(form.formState.errors.name && 'border-destructive')}
        />
        {form.formState.errors.name && (
          <p className="text-sm text-destructive">
            {form.formState.errors.name.message}
          </p>
        )}
      </div>

      <div className="flex justify-end gap-2">
        <Button type="button" variant="outline">Cancel</Button>
        <Button type="submit" disabled={form.formState.isSubmitting}>
          {form.formState.isSubmitting ? 'Saving...' : 'Save'}
        </Button>
      </div>
    </form>
  );
}
```

### Dialog Pattern
```tsx
<Dialog open={open} onOpenChange={setOpen}>
  <DialogContent className="sm:max-w-[500px]">
    <DialogHeader>
      <DialogTitle>Dialog Title</DialogTitle>
    </DialogHeader>
    <div className="space-y-4 py-4">
      {/* Form or content */}
    </div>
  </DialogContent>
</Dialog>
```

### Stats Card
```tsx
<Card>
  <CardHeader className="flex flex-row items-center justify-between pb-2">
    <CardTitle className="text-sm font-medium text-muted-foreground">
      Total Revenue
    </CardTitle>
    <DollarSign className="h-4 w-4 text-muted-foreground" />
  </CardHeader>
  <CardContent>
    <div className="text-2xl font-bold">$45,231.89</div>
    <p className="text-xs text-muted-foreground">
      <span className="text-green-500">+20.1%</span> from last month
    </p>
  </CardContent>
</Card>
```

## Design Principles

### For Field Service Context
1. **Efficiency First**: Service managers and technicians are busy - minimize clicks
2. **Scannable**: Use visual hierarchy, badges, color coding
3. **Mobile-Ready**: Works on tablets and phones in the field
4. **Information Dense**: Show relevant data without clutter
5. **Action-Oriented**: Clear CTAs, quick actions for field teams

## Creative Mode (Landing Pages / Marketing)

When building landing pages, marketing materials, or public-facing pages:
- **Break the mold**: Use unexpected layouts
- **Bold typography**: Try display fonts beyond Inter
- **Visual depth**: Gradients, shadows, animations
- **Memorable**: What makes THIS page unforgettable?

Still use Fixlify colors as accent, but don't limit creativity.

### Visual Guidelines
- **Cards** for grouping related content
- **Tables** for lists with actions
- **Badges** for status indication
- **Icons** from Lucide (consistent 16-20px)
- **Shadows** subtle (shadow-sm to shadow-md)
- **Borders** light (border-border)
- **Rounded** corners (rounded-lg)

### Status Colors
```tsx
const statusColors = {
  // Documents (Estimates/Invoices)
  draft: { bg: 'bg-slate-50', text: 'text-slate-600', border: 'border-slate-200', dot: 'bg-slate-400' },
  sent: { bg: 'bg-violet-50', text: 'text-violet-600', border: 'border-violet-200', dot: 'bg-violet-500' },
  approved: { bg: 'bg-emerald-50', text: 'text-emerald-600', border: 'border-emerald-200', dot: 'bg-emerald-500' },
  rejected: { bg: 'bg-red-50', text: 'text-red-600', border: 'border-red-200', dot: 'bg-red-500' },
  converted: { bg: 'bg-violet-50', text: 'text-violet-600', border: 'border-violet-200', dot: 'bg-violet-500' },

  // Payments
  paid: { bg: 'bg-emerald-50', text: 'text-emerald-600', border: 'border-emerald-200', dot: 'bg-emerald-500' },
  unpaid: { bg: 'bg-orange-50', text: 'text-orange-600', border: 'border-orange-200', dot: 'bg-orange-500' },
  partial: { bg: 'bg-amber-50', text: 'text-amber-600', border: 'border-amber-200', dot: 'bg-amber-500' },
  overdue: { bg: 'bg-red-50', text: 'text-red-600', border: 'border-red-200', dot: 'bg-red-500' },

  // Jobs
  pending: 'bg-amber-100 text-amber-800',
  in_progress: 'bg-violet-100 text-violet-800',
  completed: 'bg-emerald-100 text-emerald-800',
  cancelled: 'bg-slate-100 text-slate-500',

  // Priority
  low: 'bg-slate-100 text-slate-800',
  medium: 'bg-amber-100 text-amber-800',
  high: 'bg-orange-100 text-orange-800',
  urgent: 'bg-red-100 text-red-800',
};
```

## Loading & Empty States

### Skeleton Loading
```tsx
import { Skeleton } from '@/components/ui/skeleton';

<div className="space-y-3">
  <Skeleton className="h-12 w-full" />
  <Skeleton className="h-12 w-full" />
  <Skeleton className="h-12 w-full" />
</div>
```

### Empty State
```tsx
<div className="flex flex-col items-center justify-center py-12 text-center">
  <Package className="h-12 w-12 text-muted-foreground mb-4" />
  <h3 className="text-lg font-medium">No items found</h3>
  <p className="text-muted-foreground mb-4">
    Get started by creating your first item.
  </p>
  <Button>
    <Plus className="mr-2 h-4 w-4" />
    Add Item
  </Button>
</div>
```

## Responsive Breakpoints

```tsx
// Mobile first approach
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
  {/* Cards */}
</div>

// Hide on mobile
<div className="hidden md:flex">Desktop only</div>

// Stack on mobile
<div className="flex flex-col md:flex-row gap-4">
  <div className="flex-1">Left</div>
  <div className="flex-1">Right</div>
</div>
```

## Animation Patterns

```tsx
// Fade in on mount
<div className="animate-in fade-in duration-300">
  Content
</div>

// Slide up
<div className="animate-in slide-in-from-bottom-4 duration-300">
  Content
</div>

// Staggered list
{items.map((item, i) => (
  <div
    key={item.id}
    className="animate-in fade-in slide-in-from-bottom-2"
    style={{ animationDelay: `${i * 50}ms` }}
  >
    {item.name}
  </div>
))}
```

## Checklist Before Completing UI

- [ ] Responsive on mobile, tablet, desktop
- [ ] Loading states implemented
- [ ] Empty states implemented
- [ ] Error states handled
- [ ] Keyboard accessible
- [ ] Dark mode compatible (if applicable)
- [ ] Consistent with existing Fixlify patterns
- [ ] Uses shadcn/ui components where possible
- [ ] TypeScript types complete
- [ ] No console errors or warnings
