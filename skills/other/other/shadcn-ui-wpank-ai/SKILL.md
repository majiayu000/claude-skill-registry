---
name: shadcn-ui
model: fast
description: Build accessible, customizable UIs with shadcn/ui, Radix UI, and Tailwind CSS. Use when setting up shadcn/ui, installing components, building forms with React Hook Form + Zod, customizing themes, or implementing component patterns.
keywords: [shadcn, shadcn/ui, radix ui, tailwind, react components, forms, react hook form, zod, dialog, sheet, button, card, toast, select, dropdown, table, accessible components]
---

# shadcn/ui Component Patterns

Expert guide for building accessible, customizable UI components with shadcn/ui.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install shadcn-ui
```


## WHEN

- Setting up a new project with shadcn/ui
- Installing or configuring individual components
- Building forms with React Hook Form and Zod validation
- Creating accessible UI components (buttons, dialogs, dropdowns, sheets)
- Customizing component styling with Tailwind CSS
- Implementing design systems with shadcn/ui
- Building Next.js applications with TypeScript

## What is shadcn/ui?

A **collection of reusable components** you copy into your project — not an npm package. You own the code. Built on **Radix UI** (accessibility) and **Tailwind CSS** (styling).

## Quick Start

```bash
# New Next.js project
npx create-next-app@latest my-app --typescript --tailwind --eslint --app
cd my-app
npx shadcn@latest init

# Install components
npx shadcn@latest add button input form card dialog select toast
npx shadcn@latest add --all  # or install everything
```

## Core Concepts

### The `cn` Utility

Merges Tailwind classes with conflict resolution — used in every component:

```tsx
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

### Class Variance Authority (CVA)

Manages component variants — the pattern behind every shadcn/ui component:

```tsx
import { cva, type VariantProps } from "class-variance-authority"

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border border-input bg-background hover:bg-accent",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/90",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: { variant: "default", size: "default" },
  }
)
```

## Essential Components

### Button

```tsx
import { Button } from "@/components/ui/button"
import { Loader2 } from "lucide-react"

// Variants: default | destructive | outline | secondary | ghost | link
// Sizes: default | sm | lg | icon
<Button variant="outline" size="sm">Click me</Button>

// Loading state
<Button disabled>
  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
  Please wait
</Button>

// As link (uses Radix Slot)
<Button asChild>
  <a href="/dashboard">Go to Dashboard</a>
</Button>
```

### Forms with Validation

The standard pattern: Zod schema + React Hook Form + shadcn Form components.

```bash
npx shadcn@latest add form input select checkbox textarea
```

```tsx
"use client"

import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import * as z from "zod"
import { Button } from "@/components/ui/button"
import {
  Form, FormControl, FormDescription,
  FormField, FormItem, FormLabel, FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

const formSchema = z.object({
  username: z.string().min(2, "Username must be at least 2 characters."),
  email: z.string().email("Please enter a valid email."),
  role: z.enum(["admin", "user", "guest"]),
})

export function ProfileForm() {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: { username: "", email: "", role: "user" },
  })

  function onSubmit(values: z.infer<typeof formSchema>) {
    console.log(values)
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <FormField control={form.control} name="username" render={({ field }) => (
          <FormItem>
            <FormLabel>Username</FormLabel>
            <FormControl><Input placeholder="shadcn" {...field} /></FormControl>
            <FormDescription>Your public display name.</FormDescription>
            <FormMessage />
          </FormItem>
        )} />

        <FormField control={form.control} name="email" render={({ field }) => (
          <FormItem>
            <FormLabel>Email</FormLabel>
            <FormControl><Input type="email" {...field} /></FormControl>
            <FormMessage />
          </FormItem>
        )} />

        <FormField control={form.control} name="role" render={({ field }) => (
          <FormItem>
            <FormLabel>Role</FormLabel>
            <Select onValueChange={field.onChange} defaultValue={field.value}>
              <FormControl>
                <SelectTrigger><SelectValue placeholder="Select a role" /></SelectTrigger>
              </FormControl>
              <SelectContent>
                <SelectItem value="admin">Admin</SelectItem>
                <SelectItem value="user">User</SelectItem>
                <SelectItem value="guest">Guest</SelectItem>
              </SelectContent>
            </Select>
            <FormMessage />
          </FormItem>
        )} />

        <Button type="submit">Submit</Button>
      </form>
    </Form>
  )
}
```

### Dialog & Sheet

```tsx
import {
  Dialog, DialogContent, DialogDescription,
  DialogFooter, DialogHeader, DialogTitle, DialogTrigger,
} from "@/components/ui/dialog"
import {
  Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger,
} from "@/components/ui/sheet"

// Modal dialog
<Dialog>
  <DialogTrigger asChild><Button variant="outline">Edit profile</Button></DialogTrigger>
  <DialogContent className="sm:max-w-[425px]">
    <DialogHeader>
      <DialogTitle>Edit profile</DialogTitle>
      <DialogDescription>Make changes here. Click save when done.</DialogDescription>
    </DialogHeader>
    <div className="grid gap-4 py-4">{/* form fields */}</div>
    <DialogFooter><Button type="submit">Save changes</Button></DialogFooter>
  </DialogContent>
</Dialog>

// Slide-over panel (side: "left" | "right" | "top" | "bottom")
<Sheet>
  <SheetTrigger asChild><Button variant="outline">Open</Button></SheetTrigger>
  <SheetContent side="right">
    <SheetHeader><SheetTitle>Settings</SheetTitle></SheetHeader>
    {/* content */}
  </SheetContent>
</Sheet>
```

### Card

```tsx
import {
  Card, CardContent, CardDescription,
  CardFooter, CardHeader, CardTitle,
} from "@/components/ui/card"

<Card className="w-[350px]">
  <CardHeader>
    <CardTitle>Create project</CardTitle>
    <CardDescription>Deploy your new project in one-click.</CardDescription>
  </CardHeader>
  <CardContent>
    <div className="grid w-full items-center gap-4">
      <div className="flex flex-col space-y-1.5">
        <Label htmlFor="name">Name</Label>
        <Input id="name" placeholder="Project name" />
      </div>
    </div>
  </CardContent>
  <CardFooter className="flex justify-between">
    <Button variant="outline">Cancel</Button>
    <Button>Deploy</Button>
  </CardFooter>
</Card>
```

### Toast Notifications

```tsx
// 1. Add Toaster to root layout
import { Toaster } from "@/components/ui/toaster"

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}<Toaster /></body>
    </html>
  )
}

// 2. Use toast in components
import { useToast } from "@/components/ui/use-toast"
import { ToastAction } from "@/components/ui/toast"

const { toast } = useToast()

toast({ title: "Success", description: "Changes saved." })

toast({
  variant: "destructive",
  title: "Error",
  description: "Something went wrong.",
  action: <ToastAction altText="Try again">Try again</ToastAction>,
})
```

### Table

```tsx
import {
  Table, TableBody, TableCaption, TableCell,
  TableHead, TableHeader, TableRow,
} from "@/components/ui/table"

const invoices = [
  { invoice: "INV001", status: "Paid", method: "Credit Card", amount: "$250.00" },
  { invoice: "INV002", status: "Pending", method: "PayPal", amount: "$150.00" },
]

<Table>
  <TableCaption>A list of your recent invoices.</TableCaption>
  <TableHeader>
    <TableRow>
      <TableHead>Invoice</TableHead>
      <TableHead>Status</TableHead>
      <TableHead>Method</TableHead>
      <TableHead className="text-right">Amount</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    {invoices.map((invoice) => (
      <TableRow key={invoice.invoice}>
        <TableCell className="font-medium">{invoice.invoice}</TableCell>
        <TableCell>{invoice.status}</TableCell>
        <TableCell>{invoice.method}</TableCell>
        <TableCell className="text-right">{invoice.amount}</TableCell>
      </TableRow>
    ))}
  </TableBody>
</Table>
```

## Theming

shadcn/ui uses CSS variables in HSL format. Configure in `globals.css`:

```css
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --destructive: 0 84.2% 60.2%;
    --border: 214.3 31.8% 91.4%;
    --ring: 222.2 84% 4.9%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;
    /* ... mirror all variables for dark mode */
  }
}
```

Colors reference as `hsl(var(--primary))` in Tailwind config. Change the CSS variables to retheme the entire app.

## Customizing Components

Since you own the code, modify components directly:

```tsx
// Add a custom variant to button.tsx
const buttonVariants = cva("...", {
  variants: {
    variant: {
      // ... existing variants
      gradient: "bg-gradient-to-r from-purple-500 to-pink-500 text-white",
    },
    size: {
      // ... existing sizes
      xl: "h-14 rounded-md px-10 text-lg",
    },
  },
})
```

## Component Reference

| Component | Install | Key Props |
|-----------|---------|-----------|
| Button | `add button` | `variant`, `size`, `asChild` |
| Input | `add input` | Standard HTML input props |
| Form | `add form` | React Hook Form + Zod integration |
| Card | `add card` | Header, Content, Footer composition |
| Dialog | `add dialog` | Modal with trigger pattern |
| Sheet | `add sheet` | Slide-over panel, `side` prop |
| Select | `add select` | Accessible dropdown |
| Toast | `add toast` | `variant: "default" \| "destructive"` |
| Table | `add table` | Header, Body, Row, Cell composition |
| Tabs | `add tabs` | `defaultValue`, trigger/content pairs |
| Accordion | `add accordion` | `type: "single" \| "multiple"` |
| Command | `add command` | Command palette / search |
| Dropdown Menu | `add dropdown-menu` | Context menus, action menus |
| Menubar | `add menubar` | Application menus with shortcuts |

## Next.js Integration

### App Router Setup

For Next.js 13+ with App Router, ensure interactive components use `"use client"`:

```tsx
// src/components/ui/button.tsx
"use client"

import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
// ... rest of component
```

### Layout Integration

Add the Toaster to your root layout:

```tsx
// app/layout.tsx
import { Toaster } from "@/components/ui/toaster"
import "./globals.css"

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="min-h-screen bg-background font-sans antialiased">
        {children}
        <Toaster />
      </body>
    </html>
  )
}
```

### Server Components

Most shadcn/ui components need `"use client"`. For Server Components, wrap them in a client component or use them in client component children.

## CLI Reference

```bash
npx shadcn@latest init              # Initialize project
npx shadcn@latest add [component]   # Add specific component
npx shadcn@latest add --all         # Add all components
npx shadcn@latest diff              # Show upstream changes
```

## Best Practices

| Practice | Details |
|----------|---------|
| **Use TypeScript** | All components ship with full type definitions |
| **Zod for validation** | Pair with React Hook Form for type-safe forms |
| **`asChild` pattern** | Use Radix Slot to render as different elements |
| **Server Components** | Most shadcn/ui components need `"use client"` |
| **Consistent structure** | Follow the existing component patterns when customizing |
| **Accessibility** | Radix primitives handle ARIA; don't override without reason |
| **CSS variables** | Theme via variables, not by editing component classes |
| **Tree-shaking** | Only install components you need — they're independent |

## NEVER Do

| Never | Why | Instead |
|-------|-----|---------|
| Install shadcn as npm package | It's not a package — it's source code you own | Use CLI: `npx shadcn@latest add` |
| Override ARIA attributes | Radix handles accessibility correctly | Trust the primitives |
| Use inline styles for theming | Defeats the design system | Modify CSS variables |
| Copy components from docs manually | May miss dependencies | Use CLI for proper installation |
| Mix component styles | Creates inconsistency | Follow CVA variant pattern |

## References

- [Learning Guide](references/learn.md) — progression from basics to advanced patterns
- [Extended Components](references/extended-components.md) — Terminal, Dock, Charts, animations, custom hooks
- [Official Docs](https://ui.shadcn.com) | [Radix UI](https://www.radix-ui.com) | [React Hook Form](https://react-hook-form.com) | [Zod](https://zod.dev)
