---
name: shadcn-ui
description: Provides complete shadcn/ui component library patterns including installation, configuration, and implementation of accessible React components. Use when setting up shadcn/ui, installing components, building forms with React Hook Form and Zod, customizing themes with Tailwind CSS, or implementing UI patterns like buttons, dialogs, dropdowns, tables, and complex form layouts.
allowed-tools: Read, Write, Bash, Edit, Glob
---

# shadcn/ui Component Patterns

Build accessible, customizable UI components with shadcn/ui, Radix UI, and Tailwind CSS.

## Overview

- Components are **copied into your project** — you own and customize the code
- Built on **Radix UI** primitives for full accessibility
- Styled with **Tailwind CSS** and CSS variables for theming
- CLI-based installation: `npx shadcn@latest add <component>`

## When to Use

Activate when user requests involve:
- "Set up shadcn/ui", "initialize shadcn", "add shadcn components"
- "Install button/input/form/dialog/card/select/toast/table/chart"
- "React Hook Form", "Zod validation", "form with validation"
- "accessible components", "Radix UI", "Tailwind theme"
- "shadcn button", "shadcn dialog", "shadcn sheet", "shadcn table"
- "dark mode", "CSS variables", "custom theme"
- "charts with Recharts", "bar chart", "line chart", "pie chart"

## Quick Reference

### Available Components

| Component | Install Command | Description |
|-----------|----------------|-------------|
| `button` | `npx shadcn@latest add button` | Variants: default, destructive, outline, secondary, ghost, link |
| `input` | `npx shadcn@latest add input` | Text input field |
| `form` | `npx shadcn@latest add form` | React Hook Form integration with validation |
| `card` | `npx shadcn@latest add card` | Container with header, content, footer |
| `dialog` | `npx shadcn@latest add dialog` | Modal overlay |
| `sheet` | `npx shadcn@latest add sheet` | Slide-over panel (top/right/bottom/left) |
| `select` | `npx shadcn@latest add select` | Dropdown select |
| `toast` | `npx shadcn@latest add toast` | Notification toasts |
| `table` | `npx shadcn@latest add table` | Data table |
| `menubar` | `npx shadcn@latest add menubar` | Desktop-style menubar |
| `chart` | `npx shadcn@latest add chart` | Recharts wrapper with theming |
| `textarea` | `npx shadcn@latest add textarea` | Multi-line text input |
| `checkbox` | `npx shadcn@latest add checkbox` | Checkbox input |
| `label` | `npx shadcn@latest add label` | Accessible form label |

## Instructions

### Initialize Project

```bash
# New Next.js project
npx create-next-app@latest my-app --typescript --tailwind --eslint --app
cd my-app
npx shadcn@latest init

# Existing project
npm install tailwindcss-animate class-variance-authority clsx tailwind-merge lucide-react
npx shadcn@latest init

# Install components
npx shadcn@latest add button input form card dialog select toast
```

### Basic Component Usage

```tsx
// Button with variants and sizes
import { Button } from "@/components/ui/button"

<Button variant="default">Default</Button>
<Button variant="destructive" size="sm">Delete</Button>
<Button variant="outline" disabled>Loading...</Button>
```

### Form with Zod Validation

```tsx
"use client"

import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { z } from "zod"
import { Button } from "@/components/ui/button"
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"
import { Input } from "@/components/ui/input"

const formSchema = z.object({
  email: z.string().email("Invalid email"),
  password: z.string().min(8, "Password must be at least 8 characters"),
})

export function LoginForm() {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: { email: "", password: "" },
  })

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(console.log)} className="space-y-4">
        <FormField name="email" control={form.control} render={({ field }) => (
          <FormItem>
            <FormLabel>Email</FormLabel>
            <FormControl><Input type="email" {...field} /></FormControl>
            <FormMessage />
          </FormItem>
        )} />
        <FormField name="password" control={form.control} render={({ field }) => (
          <FormItem>
            <FormLabel>Password</FormLabel>
            <FormControl><Input type="password" {...field} /></FormControl>
            <FormMessage />
          </FormItem>
        )} />
        <Button type="submit">Login</Button>
      </form>
    </Form>
  )
}
```

See [references/forms-and-validation.md](references/forms-and-validation.md) for advanced multi-field forms, contact forms with API submission, and login card patterns.

### Dialog (Modal)

```tsx
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"

<Dialog>
  <DialogTrigger asChild>
    <Button variant="outline">Open</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Edit Profile</DialogTitle>
    </DialogHeader>
    {/* content */}
  </DialogContent>
</Dialog>
```

### Toast Notification

```tsx
// 1. Add <Toaster /> to app/layout.tsx
import { Toaster } from "@/components/ui/toaster"

// 2. Use in components
import { useToast } from "@/components/ui/use-toast"

const { toast } = useToast()
toast({ title: "Success", description: "Changes saved." })
toast({ variant: "destructive", title: "Error", description: "Something went wrong." })
```

### Bar Chart

```tsx
import { Bar, BarChart, CartesianGrid, XAxis } from "recharts"
import { ChartContainer, ChartTooltipContent } from "@/components/ui/chart"

const chartConfig = {
  desktop: { label: "Desktop", color: "var(--chart-1)" },
} satisfies import("@/components/ui/chart").ChartConfig

<ChartContainer config={chartConfig} className="min-h-[200px] w-full">
  <BarChart data={data}>
    <CartesianGrid vertical={false} />
    <XAxis dataKey="month" />
    <Bar dataKey="desktop" fill="var(--color-desktop)" radius={4} />
    <ChartTooltip content={<ChartTooltipContent />} />
  </BarChart>
</ChartContainer>
```

See [references/charts-components.md](references/charts-components.md) for Line, Area, and Pie chart examples.

## Examples

### Login Form with Validation
```tsx
"use client"
import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { z } from "zod"
import { Button } from "@/components/ui/button"
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"
import { Input } from "@/components/ui/input"

const formSchema = z.object({
  email: z.string().email("Invalid email"),
  password: z.string().min(8, "Min 8 characters"),
})

export function LoginForm() {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: { email: "", password: "" },
  })

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(console.log)} className="space-y-4">
        <FormField name="email" control={form.control} render={({ field }) => (
          <FormItem>
            <FormLabel>Email</FormLabel>
            <FormControl><Input type="email" {...field} /></FormControl>
            <FormMessage />
          </FormItem>
        )} />
        <FormField name="password" control={form.control} render={({ field }) => (
          <FormItem>
            <FormLabel>Password</FormLabel>
            <FormControl><Input type="password" {...field} /></FormControl>
            <FormMessage />
          </FormItem>
        )} />
        <Button type="submit">Login</Button>
      </form>
    </Form>
  )
}
```

### Data Table with Actions
```tsx
import { ColumnDef } from "@tanstack/react-table"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import { DataTable } from "@/components/ui/data-table"

const columns: ColumnDef<User>[] = [
  { id: "select", header: ({ table }) => (
    <Checkbox checked={table.getIsAllPageRowsSelected()} />
  ), cell: ({ row }) => (
    <Checkbox checked={row.getIsSelected()} />
  )},
  { accessorKey: "name", header: "Name" },
  { accessorKey: "email", header: "Email" },
  { id: "actions", cell: ({ row }) => (
    <Button variant="ghost" size="sm">Edit</Button>
  )},
]
```

### Dialog with Form
```tsx
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"

<Dialog>
  <DialogTrigger asChild>
    <Button variant="outline">Add User</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Add New User</DialogTitle>
    </DialogHeader>
    {/* <LoginForm /> */}
  </DialogContent>
</Dialog>
```

### Toast Notifications
```tsx
import { useToast } from "@/components/ui/use-toast"
import { Button } from "@/components/ui/button"

const { toast } = useToast()

toast({ title: "Saved", description: "Changes saved successfully." })
toast({ variant: "destructive", title: "Error", description: "Failed to save." })
```

## Best Practices

- **Accessibility**: Use Radix UI primitives — ARIA attributes are built in
- **Client Components**: Add `"use client"` for interactive components (hooks, events)
- **Type Safety**: Use TypeScript and Zod schemas for form validation
- **Theming**: Configure CSS variables in `globals.css` for consistent design
- **Customization**: Modify component files directly — you own the code
- **Path Aliases**: Ensure `@` alias is configured in `tsconfig.json`
- **Registry Security**: Only install components from trusted registries; review generated code before production use
- **Dark Mode**: Set up with CSS variables strategy and `next-themes`
- **Forms**: Always use `Form`, `FormField`, `FormItem`, `FormLabel`, `FormMessage` together
- **Toaster**: Add `<Toaster />` once to root layout

## Constraints and Warnings

- **Not an NPM Package**: Components are copied to your project; they are not a versioned dependency
- **Registry Security**: Components from `npx shadcn@latest add` are fetched remotely; always verify the registry source is trusted before installation
- **Client Components**: Most interactive components require `"use client"` directive
- **Radix Dependencies**: Ensure all `@radix-ui` packages are installed
- **Tailwind Required**: Components rely on Tailwind CSS utilities
- **Path Aliases**: Configure `@` alias in `tsconfig.json` for imports

## References

Consult these files for detailed patterns and code examples:

- **[references/setup-and-configuration.md](references/setup-and-configuration.md)** — Full installation, tsconfig, tailwind config, CSS variables
- **[references/ui-components.md](references/ui-components.md)** — Button, Input, Card, Dialog, Sheet, Select, Toast, Table, Menubar
- **[references/forms-and-validation.md](references/forms-and-validation.md)** — React Hook Form + Zod, advanced forms, login card, contact form
- **[references/charts-components.md](references/charts-components.md)** — Bar, Line, Area, Pie charts with ChartContainer and theming
- **[references/nextjs-integration.md](references/nextjs-integration.md)** — App Router, Server/Client Components, dark mode, metadata
- **[references/customization.md](references/customization.md)** — Custom variants, CSS variables, cn() utility, extending components
