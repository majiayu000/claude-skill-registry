---
name: styling-with-shadcn
description: |
  Build beautiful, accessible UIs with shadcn/ui components in Next.js. Use when creating
  forms, dialogs, tables, sidebars, or any UI components. Covers installation, component
  patterns, react-hook-form + Zod validation, and dark mode setup.
  NOT when building non-React applications or using different component libraries.
---

# shadcn/ui

Build beautiful, accessible UIs with copy-paste components built on Radix UI and Tailwind CSS.

## Quick Start

```bash
# Initialize shadcn/ui in your Next.js project
npx shadcn@latest init

# Add components as needed
npx shadcn@latest add button form dialog table sidebar
```

## Common Component Install

```bash
npx shadcn@latest add button card form input label dialog \
  table badge sidebar dropdown-menu avatar separator \
  select textarea tabs toast sonner
```

---

## Core Patterns

### 1. Button Variants

```tsx
import { Button } from "@/components/ui/button"

<Button variant="default">Primary</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="destructive">Delete</Button>
<Button variant="outline">Outline</Button>
<Button variant="ghost">Ghost</Button>

// Sizes: sm, default, lg, icon
<Button size="icon"><Plus /></Button>

// Loading state
<Button disabled>
  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
  Loading...
</Button>

// As Next.js Link
<Button asChild>
  <Link href="/dashboard">Go to Dashboard</Link>
</Button>
```

### 2. Forms with react-hook-form + Zod

```tsx
"use client"
import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { z } from "zod"
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"

const schema = z.object({
  title: z.string().min(1, "Required"),
  priority: z.enum(["low", "medium", "high"]),
})

export function TaskForm({ onSubmit }) {
  const form = useForm({
    resolver: zodResolver(schema),
    defaultValues: { title: "", priority: "medium" },
  })

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <FormField
          control={form.control}
          name="title"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Title</FormLabel>
              <FormControl>
                <Input {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">Submit</Button>
      </form>
    </Form>
  )
}
```

See [references/component-examples.md](references/component-examples.md) for complete form with Select, Textarea.

### 3. Dialog / Modal

```tsx
import {
  Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger
} from "@/components/ui/dialog"

<Dialog>
  <DialogTrigger asChild>
    <Button>Create Task</Button>
  </DialogTrigger>
  <DialogContent className="sm:max-w-[425px]">
    <DialogHeader>
      <DialogTitle>Create New Task</DialogTitle>
      <DialogDescription>Add a new task to your project.</DialogDescription>
    </DialogHeader>
    <TaskForm onSubmit={handleSubmit} />
  </DialogContent>
</Dialog>

// Controlled dialog
const [open, setOpen] = useState(false)
<Dialog open={open} onOpenChange={setOpen}>...</Dialog>
```

### 4. Alert Dialog (Confirmation)

```tsx
import {
  AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent,
  AlertDialogDescription, AlertDialogFooter, AlertDialogHeader,
  AlertDialogTitle, AlertDialogTrigger
} from "@/components/ui/alert-dialog"

<AlertDialog>
  <AlertDialogTrigger asChild>
    <Button variant="destructive">Delete</Button>
  </AlertDialogTrigger>
  <AlertDialogContent>
    <AlertDialogHeader>
      <AlertDialogTitle>Are you sure?</AlertDialogTitle>
      <AlertDialogDescription>This action cannot be undone.</AlertDialogDescription>
    </AlertDialogHeader>
    <AlertDialogFooter>
      <AlertDialogCancel>Cancel</AlertDialogCancel>
      <AlertDialogAction onClick={handleDelete}>Delete</AlertDialogAction>
    </AlertDialogFooter>
  </AlertDialogContent>
</AlertDialog>
```

### 5. Data Table (TanStack)

```tsx
import { ColumnDef, flexRender, getCoreRowModel, useReactTable } from "@tanstack/react-table"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

const columns: ColumnDef<Task>[] = [
  { accessorKey: "title", header: "Title" },
  {
    accessorKey: "status",
    header: "Status",
    cell: ({ row }) => <Badge>{row.getValue("status")}</Badge>,
  },
]

const table = useReactTable({
  data,
  columns,
  getCoreRowModel: getCoreRowModel(),
})
```

See [references/component-examples.md](references/component-examples.md) for full DataTable with sorting/pagination.

### 6. Card Component

```tsx
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"

<Card>
  <CardHeader>
    <CardTitle>{task.title}</CardTitle>
    <CardDescription>Assigned to {task.assignee}</CardDescription>
  </CardHeader>
  <CardContent>
    <p>{task.description}</p>
  </CardContent>
  <CardFooter>
    <Button>Start</Button>
  </CardFooter>
</Card>
```

### 7. Toast Notifications (Sonner)

```tsx
// Add Toaster to layout
import { Toaster } from "@/components/ui/sonner"
<Toaster />

// Use in components
import { toast } from "sonner"

toast.success("Task created")
toast.error("Failed to create task")
toast("Task Updated", { description: "Status changed to in progress" })
toast.promise(createTask(data), {
  loading: "Creating...",
  success: "Created!",
  error: "Failed",
})
```

### 8. Sidebar Navigation

```tsx
import {
  Sidebar, SidebarContent, SidebarGroup, SidebarGroupContent,
  SidebarMenu, SidebarMenuButton, SidebarMenuItem, SidebarProvider, SidebarTrigger
} from "@/components/ui/sidebar"

<SidebarProvider>
  <Sidebar>
    <SidebarContent>
      <SidebarMenu>
        {items.map((item) => (
          <SidebarMenuItem key={item.title}>
            <SidebarMenuButton asChild>
              <a href={item.url}><item.icon />{item.title}</a>
            </SidebarMenuButton>
          </SidebarMenuItem>
        ))}
      </SidebarMenu>
    </SidebarContent>
  </Sidebar>
  <main><SidebarTrigger />{children}</main>
</SidebarProvider>
```

See [references/component-examples.md](references/component-examples.md) for full sidebar with persistent state.

### 9. Dark Mode

```tsx
// npm install next-themes

// components/theme-provider.tsx
"use client"
import { ThemeProvider as NextThemesProvider } from "next-themes"

export function ThemeProvider({ children, ...props }) {
  return <NextThemesProvider {...props}>{children}</NextThemesProvider>
}

// layout.tsx
<ThemeProvider attribute="class" defaultTheme="system" enableSystem>
  {children}
</ThemeProvider>

// Theme toggle
import { useTheme } from "next-themes"
const { setTheme } = useTheme()
setTheme("dark") // or "light" or "system"
```

---

## Dependencies

```json
{
  "dependencies": {
    "@hookform/resolvers": "^3.x",
    "@radix-ui/react-*": "latest",
    "@tanstack/react-table": "^8.x",
    "class-variance-authority": "^0.7.x",
    "clsx": "^2.x",
    "lucide-react": "^0.x",
    "next-themes": "^0.4.x",
    "react-hook-form": "^7.x",
    "sonner": "^1.x",
    "tailwind-merge": "^2.x",
    "zod": "^3.x"
  }
}
```

---

## Verification

Run: `python3 scripts/verify.py`

Expected: `✓ styling-with-shadcn skill ready`

## If Verification Fails

1. Check: references/ folder exists with component-examples.md
2. **Stop and report** if still failing

## Related Skills

- **fetching-library-docs** - Latest shadcn/ui docs: `--library-id /shadcn-ui/ui --topic components`
- **building-nextjs-apps** - Next.js 16 patterns for app structure

## References

- [references/component-examples.md](references/component-examples.md) - Full code examples
- [references/taskflow-theme.md](references/taskflow-theme.md) - Custom theme configuration
